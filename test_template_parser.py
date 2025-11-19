"""
Test script for the Prisma template parser
Run this to verify the template system works correctly
"""

import os
import tempfile
from template_parser import PrismaTemplate, apply_template


def test_basic_template():
    """Test basic template operations"""
    print("Testing basic template operations...")

    # Create a test template
    template_content = """# Test Template
@target test_output.txt

@line 5
This is line 5 with color: {color0}

@lines 10-12
Line 10: {background}
Line 11: {foreground}
Line 12: {color1}

@match ".*theme.*"
theme = {color2}

@append
# End of file
"""

    # Create test colors
    test_colors = {
        "color0": "#ff0000",
        "color1": "#00ff00",
        "color2": "#0000ff",
        "background": "#000000",
        "foreground": "#ffffff"
    }

    # Create temporary template file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.prisma', delete=False, encoding='utf-8') as f:
        f.write(template_content)
        template_path = f.name

    # Create temporary output file with existing content
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
        f.write("Line 1\nLine 2\nLine 3 with theme setting\nLine 4\n")
        output_path = f.name

    try:
        # Apply template
        template = PrismaTemplate(template_path)
        template.apply(test_colors, output_path)

        # Read result
        with open(output_path, 'r', encoding='utf-8') as f:
            result = f.read()

        print("✓ Template applied successfully")
        print("\nOutput:")
        print("-" * 50)
        print(result)
        print("-" * 50)

        # Verify some key content
        assert "#ff0000" in result, "color0 not substituted"
        assert "#000000" in result, "background not substituted"
        assert "theme = #0000ff" in result, "@match not working"
        assert "End of file" in result, "@append not working"

        print("✓ All assertions passed")
        return True

    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        # Cleanup
        try:
            os.unlink(template_path)
            os.unlink(output_path)
        except:
            pass


def test_rgb_components():
    """Test RGB and HLS component substitution"""
    print("\nTesting RGB/HLS component substitution...")

    template_content = """@target test_rgb.txt

@line 1
Red: {color1.r}

@line 2
Green: {color1.g}

@line 3
Blue: {color1.b}

@line 4
Hue: {color1.h}
"""

    test_colors = {
        "color1": "#ff8800"  # Orange
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.prisma', delete=False, encoding='utf-8') as f:
        f.write(template_content)
        template_path = f.name

    output_path = tempfile.mktemp()

    try:
        template = PrismaTemplate(template_path)
        template.apply(test_colors, output_path)

        with open(output_path, 'r', encoding='utf-8') as f:
            result = f.read()

        print("✓ RGB/HLS template applied")
        print("\nOutput:")
        print("-" * 50)
        print(result)
        print("-" * 50)

        # Verify RGB values
        assert "Red: 255" in result, "Red component not correct"
        assert "Green: 136" in result, "Green component not correct"
        assert "Blue: 0" in result, "Blue component not correct"

        print("✓ RGB component tests passed")
        return True

    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        try:
            os.unlink(template_path)
            if os.path.exists(output_path):
                os.unlink(output_path)
        except:
            pass


def test_match_pattern():
    """Test regex pattern matching"""
    print("\nTesting regex pattern matching...")

    template_content = """@target test_match.txt

@match ".*primary.*"
primary-color = {color0}

@match ".*secondary.*"
secondary-color = {color1}
"""

    test_colors = {
        "color0": "#aabbcc",
        "color1": "#ddeeff"
    }

    # Create test file with existing content
    existing_content = """config_file
primary = #000000
other_setting = true
secondary = #111111
end
"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.prisma', delete=False, encoding='utf-8') as f:
        f.write(template_content)
        template_path = f.name

    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
        f.write(existing_content)
        output_path = f.name

    try:
        template = PrismaTemplate(template_path)
        template.apply(test_colors, output_path)

        with open(output_path, 'r', encoding='utf-8') as f:
            result = f.read()

        print("✓ Pattern matching applied")
        print("\nOutput:")
        print("-" * 50)
        print(result)
        print("-" * 50)

        assert "primary-color = #aabbcc" in result, "Primary pattern not matched"
        assert "secondary-color = #ddeeff" in result, "Secondary pattern not matched"
        assert "other_setting = true" in result, "Other content was lost"

        print("✓ Pattern matching tests passed")
        return True

    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        try:
            os.unlink(template_path)
            os.unlink(output_path)
        except:
            pass


if __name__ == "__main__":
    print("=" * 60)
    print("Prisma Template Parser Test Suite")
    print("=" * 60)

    results = []
    results.append(("Basic Operations", test_basic_template()))
    results.append(("RGB Components", test_rgb_components()))
    results.append(("Pattern Matching", test_match_pattern()))

    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)

    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name}: {status}")

    all_passed = all(result[1] for result in results)
    print("\n" + ("All tests passed! ✓" if all_passed else "Some tests failed ✗"))

    exit(0 if all_passed else 1)
