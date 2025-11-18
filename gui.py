import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from json import loads
from os import path
import sys
from main import gen_colors, get_wallpaper, home

class PrismaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Prisma - Pywal Color Generator")
        self.root.geometry("800x700")

        # State variables
        self.current_image_path = None
        self.light_mode = False
        self.colors = {}

        # Load existing pywal colors if available
        self.load_pywal_colors()

        # Set background color
        bg_color = self.colors.get("background", "#000000")
        self.root.configure(bg=bg_color)

        # Create GUI elements
        self.create_widgets()

        # Load current wallpaper
        self.load_current_wallpaper()

    def load_pywal_colors(self):
        """Load colors from pywal cache if it exists"""
        colors_path = home + "/.cache/wal/colors.json"
        if path.isfile(colors_path):
            try:
                with open(colors_path, "r") as f:
                    data = loads(f.read())
                    self.colors = data.get("colors", {})
                    self.colors.update(data.get("special", {}))
            except Exception as e:
                print(f"Could not load colors: {e}")
                self.colors = {}

        # Use gray defaults if no colors loaded
        if not self.colors:
            self.colors = {
                "background": "#000000",
                "foreground": "#808080",
                **{f"color{i}": "#808080" for i in range(16)}
            }

    def create_widgets(self):
        """Create all GUI widgets"""
        bg_color = self.colors.get("background", "#000000")
        fg_color = self.colors.get("foreground", "#ffffff")

        # Image preview section
        preview_frame = tk.Frame(self.root, bg=bg_color)
        preview_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        preview_label = tk.Label(preview_frame, text="Image Preview",
                                bg=bg_color, fg=fg_color, font=("Arial", 12, "bold"))
        preview_label.pack()

        self.image_label = tk.Label(preview_frame, bg=bg_color,
                                    text="Loading...", fg=fg_color)
        self.image_label.pack(pady=5)

        # Color grid section
        color_frame = tk.Frame(self.root, bg=bg_color)
        color_frame.pack(pady=10, padx=10)

        grid_label = tk.Label(color_frame, text="Color Palette",
                             bg=bg_color, fg=fg_color, font=("Arial", 12, "bold"))
        grid_label.pack()

        # Create grid container
        grid_container = tk.Frame(color_frame, bg=bg_color)
        grid_container.pack(pady=5)

        # Store color labels for updates
        self.color_labels = {}

        # Row 1: background/foreground, color0/1, color2/3, ..., color12/13
        # Row 2: (empty), color14/15, and remaining pairs
        color_pairs = [
            ("background", "foreground"),
            ("color0", "color1"),
            ("color2", "color3"),
            ("color4", "color5"),
            ("color6", "color7"),
            ("color8", "color9"),
            ("color10", "color11"),
            ("color12", "color13")
        ]

        for col, (color1, color2) in enumerate(color_pairs):
            # First color (top row)
            color1_val = self.colors.get(color1, "#808080")
            frame1 = tk.Frame(grid_container, bg=color1_val,
                            width=80, height=60, relief=tk.RAISED, borderwidth=2)
            frame1.grid(row=0, column=col, padx=2, pady=2)
            frame1.pack_propagate(False)

            label1 = tk.Label(frame1, text=color1, bg=color1_val,
                            fg=self.get_contrast_color(color1_val),
                            font=("Arial", 8))
            label1.pack(expand=True)
            self.color_labels[color1] = (frame1, label1)

            # Second color (bottom row)
            color2_val = self.colors.get(color2, "#808080")
            frame2 = tk.Frame(grid_container, bg=color2_val,
                            width=80, height=60, relief=tk.RAISED, borderwidth=2)
            frame2.grid(row=1, column=col, padx=2, pady=2)
            frame2.pack_propagate(False)

            label2 = tk.Label(frame2, text=color2, bg=color2_val,
                            fg=self.get_contrast_color(color2_val),
                            font=("Arial", 8))
            label2.pack(expand=True)
            self.color_labels[color2] = (frame2, label2)

        # Add color14 and color15 in the last column
        color14_val = self.colors.get("color14", "#808080")
        frame14 = tk.Frame(grid_container, bg=color14_val,
                          width=80, height=60, relief=tk.RAISED, borderwidth=2)
        frame14.grid(row=0, column=8, padx=2, pady=2)
        frame14.pack_propagate(False)

        label14 = tk.Label(frame14, text="color14", bg=color14_val,
                          fg=self.get_contrast_color(color14_val),
                          font=("Arial", 8))
        label14.pack(expand=True)
        self.color_labels["color14"] = (frame14, label14)

        color15_val = self.colors.get("color15", "#808080")
        frame15 = tk.Frame(grid_container, bg=color15_val,
                          width=80, height=60, relief=tk.RAISED, borderwidth=2)
        frame15.grid(row=1, column=8, padx=2, pady=2)
        frame15.pack_propagate(False)

        label15 = tk.Label(frame15, text="color15", bg=color15_val,
                          fg=self.get_contrast_color(color15_val),
                          font=("Arial", 8))
        label15.pack(expand=True)
        self.color_labels["color15"] = (frame15, label15)

        # Controls section
        controls_frame = tk.Frame(self.root, bg=bg_color)
        controls_frame.pack(pady=10, padx=10)

        # Light mode toggle
        self.light_mode_var = tk.BooleanVar(value=self.light_mode)
        light_toggle = tk.Checkbutton(controls_frame, text="Light Mode",
                                     variable=self.light_mode_var,
                                     command=self.toggle_light_mode,
                                     bg=bg_color, fg=fg_color,
                                     selectcolor=bg_color,
                                     font=("Arial", 10))
        light_toggle.pack(pady=5)

        # Buttons section
        button_frame = tk.Frame(self.root, bg=bg_color)
        button_frame.pack(pady=10, padx=10)

        select_btn = tk.Button(button_frame, text="Select File",
                              command=self.select_file,
                              bg=self.colors.get("color4", "#4080ff"),
                              fg=fg_color, font=("Arial", 11, "bold"),
                              padx=20, pady=10, relief=tk.RAISED)
        select_btn.pack(side=tk.LEFT, padx=10)

        generate_btn = tk.Button(button_frame, text="Generate",
                                command=self.generate_colors,
                                bg=self.colors.get("color2", "#40ff80"),
                                fg=fg_color, font=("Arial", 11, "bold"),
                                padx=20, pady=10, relief=tk.RAISED)
        generate_btn.pack(side=tk.LEFT, padx=10)

    def get_contrast_color(self, hex_color):
        """Get contrasting text color (black or white) for a given background color"""
        try:
            # Remove # if present
            hex_color = hex_color.lstrip('#')
            # Convert to RGB
            r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
            # Calculate luminance
            luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            return "#000000" if luminance > 0.5 else "#ffffff"
        except:
            return "#ffffff"

    def load_current_wallpaper(self):
        """Load and display current Windows wallpaper"""
        try:
            wallpaper_path = get_wallpaper()
            if wallpaper_path and path.isfile(wallpaper_path):
                self.current_image_path = wallpaper_path
                self.display_image(wallpaper_path)
            else:
                self.image_label.config(text="No wallpaper found")
        except Exception as e:
            self.image_label.config(text=f"Could not load wallpaper")
            print(f"Error loading wallpaper: {e}")

    def display_image(self, image_path):
        """Display image in preview area"""
        try:
            # Open and resize image
            img = Image.open(image_path)

            # Calculate aspect ratio and resize
            max_width, max_height = 400, 200
            img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(img)

            # Update label
            self.image_label.config(image=photo, text="")
            self.image_label.image = photo  # Keep a reference

        except Exception as e:
            self.image_label.config(text=f"Error loading image")
            print(f"Error displaying image: {e}")

    def select_file(self):
        """Open file dialog to select an image"""
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            self.current_image_path = file_path
            self.display_image(file_path)

    def toggle_light_mode(self):
        """Toggle between light and dark mode"""
        self.light_mode = self.light_mode_var.get()

    def generate_colors(self):
        """Generate colors from current image"""
        if not self.current_image_path:
            messagebox.showerror("Error", "No image selected. Please select an image first.")
            return

        if not path.isfile(self.current_image_path):
            messagebox.showerror("Error", "Selected image file does not exist.")
            return

        try:
            # Generate colors using main.py function
            gen_colors(self.current_image_path, apply_config=False, light_mode=self.light_mode)

            # Reload colors
            self.load_pywal_colors()

            # Update UI
            self.update_colors()

            messagebox.showinfo("Success", "Colors generated successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate colors: {str(e)}")
            print(f"Error generating colors: {e}")

    def update_colors(self):
        """Update all color displays in the GUI"""
        bg_color = self.colors.get("background", "#000000")
        fg_color = self.colors.get("foreground", "#ffffff")

        # Update root background
        self.root.configure(bg=bg_color)

        # Update all color labels
        for color_name, (frame, label) in self.color_labels.items():
            color_val = self.colors.get(color_name, "#808080")
            frame.config(bg=color_val)
            label.config(bg=color_val, fg=self.get_contrast_color(color_val))

        # Update all frames
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.config(bg=bg_color)
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame):
                        child.config(bg=bg_color)
                    elif isinstance(child, tk.Label) and child != self.image_label:
                        child.config(bg=bg_color, fg=fg_color)
                    elif isinstance(child, tk.Checkbutton):
                        child.config(bg=bg_color, fg=fg_color, selectcolor=bg_color)

def main():
    root = tk.Tk()
    app = PrismaGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
