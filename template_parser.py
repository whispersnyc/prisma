"""
Prismo Template Parser
Parses .prismo template files and applies them to target files
"""

import re
import os
from typing import Dict, List, Tuple, Optional
from colorsys import rgb_to_hls


class TemplateOperation:
    """Represents a single template operation"""
    def __init__(self, op_type: str, content: str, **kwargs):
        self.op_type = op_type  # 'line', 'lines', 'match', 'append', 'prepend'
        self.content = content
        self.params = kwargs


class PrismoTemplate:
    """Parses and applies .prismo template files"""

    def __init__(self, template_path: str):
        self.template_path = template_path
        self.operations: List[TemplateOperation] = []
        self._parse()

    def _parse(self):
        """Parse the .prismo template file"""
        with open(self.template_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        i = 0
        while i < len(lines):
            line = lines[i].rstrip('\n')

            # Skip empty lines and comments (outside content blocks)
            if not line or line.strip().startswith('#'):
                i += 1
                continue

            # Parse directives
            if line.startswith('@'):
                parts = line[1:].split(None, 1)
                directive = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ''

                # Collect content for this directive
                content_lines = []
                i += 1
                while i < len(lines):
                    if lines[i].startswith('@'):
                        break
                    content_lines.append(lines[i].rstrip('\n'))
                    i += 1

                # Remove trailing empty lines from content
                while content_lines and not content_lines[-1]:
                    content_lines.pop()

                content = '\n'.join(content_lines)

                # Create operation based on directive
                if directive == 'full':
                    # Replace entire file with content
                    self.operations.append(TemplateOperation('full', content))

                elif directive == 'line':
                    line_num = int(args.strip())
                    self.operations.append(TemplateOperation('line', content, line_num=line_num))

                elif directive == 'lines':
                    match = re.match(r'(\d+)-(\d+)', args.strip())
                    if match:
                        start, end = int(match.group(1)), int(match.group(2))
                        self.operations.append(TemplateOperation('lines', content, start=start, end=end))

                elif directive == 'match':
                    # Remove quotes from pattern
                    pattern = args.strip().strip('"').strip("'")
                    self.operations.append(TemplateOperation('match', content, pattern=pattern))

                elif directive == 'append':
                    self.operations.append(TemplateOperation('append', content))

                elif directive == 'prepend':
                    self.operations.append(TemplateOperation('prepend', content))
            else:
                i += 1

    def apply(self, colors: Dict[str, str], output_path: str):
        """
        Apply the template with color substitutions

        Args:
            colors: Dictionary of color names to hex values (from wal)
            output_path: Target file path (from config)
        """
        if not output_path:
            raise ValueError("No target path specified")

        # Expand user home directory and environment variables
        target = os.path.expandvars(os.path.expanduser(output_path))

        # Read existing file or start with empty
        if os.path.exists(target):
            try:
                with open(target, 'r', encoding='utf-8') as f:
                    file_lines = f.read().split('\n')
            except UnicodeDecodeError:
                # Try with different encodings
                try:
                    with open(target, 'r', encoding='cp850') as f:
                        file_lines = f.read().split('\n')
                except:
                    # Last resort: binary read and decode with errors ignored
                    with open(target, 'r', encoding='utf-8', errors='ignore') as f:
                        file_lines = f.read().split('\n')
        else:
            file_lines = []

        # Apply each operation
        for op in self.operations:
            # Substitute color variables in content
            content = self._substitute_colors(op.content, colors)

            if op.op_type == 'full':
                # Replace entire file with content
                file_lines = content.split('\n')

            elif op.op_type == 'line':
                line_num = op.params['line_num']
                if line_num < 1:
                    raise ValueError(f"Line number must be >= 1, got {line_num}")
                # Ensure file has enough lines
                while len(file_lines) < line_num:
                    file_lines.append('')
                file_lines[line_num - 1] = content

            elif op.op_type == 'lines':
                start = op.params['start']
                end = op.params['end']
                if start < 1 or end < 1:
                    raise ValueError(f"Line numbers must be >= 1, got start={start}, end={end}")
                if start > end:
                    raise ValueError(f"Start line ({start}) must be <= end line ({end})")
                # Ensure file has enough lines
                while len(file_lines) < end:
                    file_lines.append('')

                # Split content into lines
                new_lines = content.split('\n')
                # Replace the range (inclusive)
                file_lines[start-1:end] = new_lines

            elif op.op_type == 'match':
                pattern = op.params['pattern']
                try:
                    regex = re.compile(pattern)
                except re.error as e:
                    raise ValueError(f"Invalid regex pattern '{pattern}': {e}")

                new_lines = content.split('\n')

                # Replace all matching lines
                i = 0
                matches_found = 0
                while i < len(file_lines):
                    if regex.search(file_lines[i]):
                        # Replace with new content (could be multiple lines)
                        file_lines[i:i+1] = new_lines
                        i += len(new_lines)
                        matches_found += 1
                    else:
                        i += 1

                # Note: Not raising an error if no matches found, as this might be intentional

            elif op.op_type == 'append':
                content_lines = content.split('\n')
                file_lines.extend(content_lines)

            elif op.op_type == 'prepend':
                content_lines = content.split('\n')
                file_lines = content_lines + file_lines

        # Write result - create directory if it doesn't exist
        target_dir = os.path.dirname(target)
        if target_dir:  # Only create if there is a directory component
            os.makedirs(target_dir, exist_ok=True)

        with open(target, 'w', encoding='utf-8') as f:
            f.write('\n'.join(file_lines))

    def _substitute_colors(self, content: str, colors: Dict[str, str]) -> str:
        """Substitute color variables in content"""
        result = content

        for color_name, color_hex in colors.items():
            # Strip leading # from color_hex for better applicability
            color_hex_no_hash = color_hex.lstrip('#')

            # Replace full color {colorN}
            result = result.replace(f'{{{color_name}}}', color_hex_no_hash)

            # Replace component colors if present
            if f'{{{color_name}.' in result:
                # Convert hex to RGB (use stripped version)
                rgb = self._hex_to_rgb(color_hex_no_hash)
                # Convert RGB to HLS
                hls = rgb_to_hls(*[c / 255.0 for c in rgb])
                hls_values = [
                    hls[0] * 360,      # Hue (0-360)
                    hls[1] * 100,      # Lightness (0-100%)
                    hls[2] * 100       # Saturation (0-100%)
                ]

                # Replace RGB components
                result = result.replace(f'{{{color_name}.r}}', str(rgb[0]))
                result = result.replace(f'{{{color_name}.g}}', str(rgb[1]))
                result = result.replace(f'{{{color_name}.b}}', str(rgb[2]))

                # Replace HLS components
                result = result.replace(f'{{{color_name}.h}}', f'{hls_values[0]}')
                result = result.replace(f'{{{color_name}.l}}', f'{hls_values[1]}%')
                result = result.replace(f'{{{color_name}.s}}', f'{hls_values[2]}%')

        return result

    @staticmethod
    def _hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def apply_template(template_path: str, colors: Dict[str, str], output_path: str):
    """
    Convenience function to apply a template

    Args:
        template_path: Path to .prismo template file
        colors: Dictionary of color names to hex values
        output_path: Target file path (from config)
    """
    template = PrismoTemplate(template_path)
    template.apply(colors, output_path)
