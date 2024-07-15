import tkinter as tk
from tkinter import filedialog, messagebox, Scale, Toplevel, simpledialog
from PIL import Image, ImageTk, ImageEnhance, ImageDraw, ImageFont

class ImageViewer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Image Viewer")
        self.geometry("800x600")

        # Canvas for displaying the image
        self.canvas = tk.Canvas(self)
        self.canvas.pack(expand=True, fill="both")

        # Menu bar
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_image, accelerator="Ctrl+N")
        file_menu.add_command(label="Save", command=self.save_image, accelerator="Ctrl+S")
        file_menu.add_command(label="Export As...", command=self.export_image, accelerator="Ctrl+E")
        file_menu.add_command(label="Exit", command=self.quit, accelerator="Alt+F4")

        # Edit menu
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Rotate Right", command=self.rotate_right, accelerator="Ctrl+Shift+R")
        edit_menu.add_command(label="Rotate Left", command=self.rotate_left, accelerator="Ctrl+R")
        edit_menu.add_command(label="Crop", command=self.start_crop)
        edit_menu.add_command(label="Add Text", command=self.add_text, accelerator="Ctrl+T")
        edit_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_command(label="Adjustments", command=self.open_adjustments_window)

        # View menu
        view_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Zoom In", command=self.zoom_in, accelerator="Ctrl++")
        view_menu.add_command(label="Zoom Out", command=self.zoom_out, accelerator="Ctrl+-")

        # Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Keyboard Shortcuts", command=self.show_shortcuts)

        # Attributes for image manipulation
        self.rotation_count = 0
        self.original_image = None
        self.display_image = None
        self.image_history = []
        self.history_index = -1
        self.zoom_factor = 1.0

        # Keyboard shortcuts
        self.bind_all("<Control-n>", self.open_image)
        self.bind_all("<Control-s>", self.save_image)
        self.bind_all("<Control-e>", self.export_image)
        self.bind_all("<Alt-F4>", self.quit)
        self.bind_all("<Control-Shift-r>", self.rotate_right)
        self.bind_all("<Control-r>", self.rotate_left)
        self.bind_all("<Control-t>", self.add_text)
        self.bind_all("<Control-z>", self.undo)
        self.bind_all("<Control-y>", self.redo)
        self.bind_all("<Control-equal>", self.zoom_in)
        self.bind_all("<Control-minus>", self.zoom_out)

        # Cropping adjustments
        self.cropping = False
        self.crop_start = (0, 0)
        self.crop_rectangle = None

    def open_image(self, event=None):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
        if file_path:
            image = Image.open(file_path)
            self.original_image = image.copy()
            self.display_image = self.original_image.copy()
            self.rotation_count = 0
            self.zoom_factor = 1.0
            self.update_image()
            self.save_to_history()

    def update_image(self):
        if self.display_image:
            rotated_image = self.display_image.rotate(-90 * self.rotation_count, expand=True)
            resized_image = rotated_image.resize(
                (int(rotated_image.width * self.zoom_factor), int(rotated_image.height * self.zoom_factor)),
                Image.Resampling.LANCZOS
            )
            photo = ImageTk.PhotoImage(resized_image)

            self.canvas.config(width=photo.width(), height=photo.height())
            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvas.image = photo

    def rotate_right(self, event=None):
        self.rotation_count += 1
        self.update_image()
        self.save_to_history()

    def rotate_left(self, event=None):
        self.rotation_count -= 1
        self.update_image()
        self.save_to_history()

    def save_image(self, event=None):
        if self.display_image:
            file_types = [
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg;*.jpeg"),
                ("GIF files", "*.gif"),
                ("BMP files", "*.bmp"),
                ("All files", "*.*")
            ]
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                initialfile="edited.png",
                filetypes=file_types
            )
            if file_path:
                rotated_image = self.display_image.rotate(-90 * self.rotation_count, expand=True)
                rotated_image.save(file_path)
                self.save_to_history()

    def export_image(self, event=None):
        if self.display_image:
            file_types = [
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("GIF files", "*.gif"),
                ("BMP files", "*.bmp"),
                ("Meme image format bruh", "*.bruh"),
                ("All files", "*.*")
            ]
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                initialfile="edited.png",
                filetypes=file_types
            )
            if file_path:
                rotated_image = self.display_image.rotate(-90 * self.rotation_count, expand=True)
                rotated_image.save(file_path)
                self.save_to_history()

    def show_shortcuts(self):
        shortcuts_info = (
            "Ctrl+N - Open Image\n"
            "Ctrl+S - Save Image\n"
            "Ctrl+E - Export Image\n"
            "Alt+F4 - Exit\n"
            "Ctrl+Shift+R - Rotate Right\n"
            "Ctrl+R - Rotate Left\n"
            "Ctrl+T - Add Text\n"
            "Ctrl+Z - Undo\n"
            "Ctrl+Y - Redo\n"
            "Ctrl++ - Zoom In\n"
            "Ctrl+- - Zoom Out"
        )
        messagebox.showinfo("Keyboard Shortcuts", shortcuts_info)

    def show_about(self):
        about_info = (
            "Image Viewer\n\n"
            "A simple image viewer and editor\n"
            "Version 1.5\n"
            "© 2024 Teymur Babayev"
        )
        messagebox.showinfo("About", about_info)

    def start_crop(self):
        if self.display_image:
            self.cropping = True
            self.canvas.bind("<Button-1>", self.crop_start_position)
            self.canvas.bind("<B1-Motion>", self.crop_drag)
            self.canvas.bind("<ButtonRelease-1>", self.crop_end)

    def crop_start_position(self, event):
        self.crop_start = (event.x, event.y)

    def crop_drag(self, event):
        if self.crop_rectangle:
            self.canvas.delete(self.crop_rectangle)

        x, y = self.crop_start
        x1, y1 = (event.x, event.y)

        self.crop_rectangle = self.canvas.create_rectangle(x, y, x1, y1, outline="red", dash=(2, 2))

    def crop_end(self, event):
        if self.crop_rectangle:
            self.canvas.delete(self.crop_rectangle)
            x, y = self.crop_start
            x1, y1 = (event.x, event.y)

            rotated_image = self.display_image.rotate(-90 * self.rotation_count, expand=True)
            cropped_image = rotated_image.crop((x, y, x1, y1))
            self.original_image = cropped_image
            self.display_image = self.original_image.copy()
            self.cropping = False
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<ButtonRelease-1>")
            self.save_to_history()
            self.update_image()

    def save_to_history(self):
        if self.original_image:
            # If we are undoing, discard any redo history beyond the current position
            if self.history_index < len(self.image_history) - 1:
                self.image_history = self.image_history[:self.history_index + 1]

            # Save a copy of the current image
            self.image_history.append(self.original_image.copy())
            self.history_index = len(self.image_history) - 1

    def undo(self, event=None):
        if self.history_index > 0:
            self.history_index -= 1
            self.original_image = self.image_history[self.history_index].copy()
            self.display_image = self.original_image.copy()
            self.update_image()

    def redo(self, event=None):
        if self.history_index < len(self.image_history) - 1:
            self.history_index += 1
            self.original_image = self.image_history[self.history_index].copy()
            self.display_image = self.original_image.copy()
            self.update_image()

    def open_adjustments_window(self):
        adjustments_window = Toplevel(self)
        adjustments_window.title("Adjustments")
        adjustments_window.geometry("300x600")
        brightness_label = tk.Label(adjustments_window, text="Brightness")
        brightness_slider = Scale(adjustments_window, from_=0.1, to=2.0, resolution=0.1, orient=tk.HORIZONTAL)
        brightness_slider.set(1.0)

        contrast_label = tk.Label(adjustments_window, text="Contrast")
        contrast_slider = Scale(adjustments_window, from_=0.1, to=2.0, resolution=0.1, orient=tk.HORIZONTAL)
        contrast_slider.set(1.0)

        saturation_label = tk.Label(adjustments_window, text="Saturation")
        saturation_slider = Scale(adjustments_window, from_=0.1, to=2.0, resolution=0.1, orient=tk.HORIZONTAL)
        saturation_slider.set(1.0)

        hue_label = tk.Label(adjustments_window, text="Hue")
        hue_slider = Scale(adjustments_window, from_=-0.5, to=0.5, resolution=0.05, orient=tk.HORIZONTAL)
        hue_slider.set(0.0)

        apply_adjustments_button = tk.Button(adjustments_window, text="Apply Adjustments", command=lambda: self.apply_adjustments(
            brightness_slider.get(),
            contrast_slider.get(),
            saturation_slider.get(),
            hue_slider.get()
        ))

        # Pack adjustments widgets
        brightness_label.pack(pady=(10, 0))
        brightness_slider.pack(pady=(0, 10))
        contrast_label.pack(pady=(10, 0))
        contrast_slider.pack(pady=(0, 10))
        saturation_label.pack(pady=(10, 0))
        saturation_slider.pack(pady=(0, 10))
        hue_label.pack(pady=(10, 0))
        hue_slider.pack(pady=(0, 10))
        apply_adjustments_button.pack(pady=(10, 0))

    def apply_adjustments(self, brightness, contrast, saturation, hue):
        if self.original_image:
            enhanced_image = self.original_image.copy()
            enhanced_image = ImageEnhance.Brightness(enhanced_image).enhance(brightness)
            enhanced_image = ImageEnhance.Contrast(enhanced_image).enhance(contrast)
            enhanced_image = ImageEnhance.Color(enhanced_image).enhance(saturation)
            
            if hue != 0.0:
                enhanced_image = self.adjust_hue(enhanced_image, hue)
            
            self.display_image = enhanced_image
            self.update_image()
            self.save_to_history()

    def adjust_hue(self, image, hue_factor):
        if hue_factor == 0.0:
            return image
        
        # Convert image to HSV mode
        hsv_image = image.convert('HSV')

        # Adjust hue
        hue = ImageEnhance.Color(hsv_image).enhance(hue_factor)

        # Convert back to RGB
        return hue.convert('RGB')

    def add_text(self, event=None):
        if self.display_image:
            text = simpledialog.askstring("Add Text", "Enter text to add:")
            if text:
                font_size = 30
                font = ImageFont.truetype("arial.ttf", font_size)
                image = self.display_image.copy()
                draw = ImageDraw.Draw(image)
                
                # Calculate text position
                text_width, text_height = draw.textsize(text, font=font)
                position = ((image.width - text_width) // 2, (image.height - text_height) // 2)
                
                # Draw text on image
                draw.text(position, text, font=font, fill="white")
                
                self.original_image = image
                self.display_image = self.original_image.copy()
                self.update_image()
                self.save_to_history()

    def zoom_in(self, event=None):
        if self.zoom_factor < 2.0:
            self.zoom_factor += 0.1
            self.update_image()

    def zoom_out(self, event=None):
        if self.zoom_factor > 0.1:
            self.zoom_factor -= 0.1
            self.update_image()


if __name__ == "__main__":
    app = ImageViewer()
    app.mainloop()
