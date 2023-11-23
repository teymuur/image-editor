import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageViewer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Image Viewer")
        self.geometry("800x600")

        self.image_label = tk.Label(self)
        self.image_label.pack(expand="true")

        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        #file menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_image)
        file_menu.add_command(label="Save", command=self.save_image)
        file_menu.add_command(label="Exit", command=self.quit)

        #edit menu
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Rotate Right", command=self.rotate_right)
        edit_menu.add_command(label="Rotate Left", command=self.rotate_left)
        edit_menu.add_command(label="Crop", command=self.crop_image)

        #help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Keyboard Shortcuts", command=self.show_shortcuts)
        self.rotation_count = 0
        self.original_image = None

        #Keyboard shortcuts
        self.bind_all("<Control-o>", lambda event: self.open_image())
        self.bind_all("<Control-s>", lambda event: self.save_image())
        self.bind_all("<Alt-F4>", lambda event: self.quit())
        self.bind_all("<Control-Shift-R>", lambda event: self.rotate_right())
        self.bind_all("<Control-R>", lambda event: self.rotate_left())
        
        #cropping adjustments
        self.cropping = False
        self.crop_start = (0, 0)
        self.crop_rectangle = None

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
        if file_path:
            image = Image.open(file_path)
            self.original_image = image.copy()
            self.rotation_count = 0
            self.update_image()

    def update_image(self):
        if hasattr(self, 'original_image'):
            rotated_image = self.original_image.rotate(90 * self.rotation_count)
            photo = ImageTk.PhotoImage(rotated_image)

            self.image_label.config(image=photo)
            self.image_label.image = photo

    def rotate_right(self):
        self.rotation_count -= 1
        self.update_image()

    def rotate_left(self):
        self.rotation_count += 1
        self.update_image()

    def save_image(self):
        if hasattr(self, 'original_image'):
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
                rotated_image = self.original_image.rotate(90 * self.rotation_count)
                rotated_image.save(file_path)
    def crop_image(self):
        if hasattr(self, 'original_image'):
            self.cropping = not self.cropping

            if self.cropping:
                messagebox.showinfo("Crop", "Click and drag to select a region for cropping.")
            else:
                self.apply_crop()

    def apply_crop(self, event=None):
        if self.cropping and self.crop_start:
            x1, y1, x2, y2 = self.crop_start[0], self.crop_start[1], event.x, event.y

            # Convert coordinates to rotated image coordinates
            rotated_image = self.original_image.rotate(90 * self.rotation_count)
            width, height = rotated_image.size
            x1, y1 = min(x1, x2), min(y1, y2)
            x2, y2 = max(x1, x2), max(y1, y2)

            x1, y1 = int(x1 * width / self.image_label.winfo_width()), int(y1 * height / self.image_label.winfo_height())
            x2, y2 = int(x2 * width / self.image_label.winfo_width()), int(y2 * height / self.image_label.winfo_height())

            cropped_image = rotated_image.crop((x1, y1, x2, y2))
            self.original_image = cropped_image
            self.rotation_count = 0
            self.cropping = False
            self.crop_start = None
            self.crop_rectangle = None
            self.update_image()


    def show_shortcuts(self):
        shortcuts_info = (
            "Ctrl+O - Open Image\n"
            "Ctrl+S - Save Image\n"
            "Alt+F4 - Exit\n"
            "Ctrl+Shift+R - Rotate Right\n"
            "Ctrl+R - Rotate Left"
        )
        messagebox.showinfo("Keyboard Shortcuts", shortcuts_info)

    def show_about(self):
        about_info = (
            "Image Viewer\n\n"
            "A simple image viewer and editor\n"
            "Version 1.0\n"
            "© 2023 Teymur Babayev"
        )
        messagebox.showinfo("About", about_info)
if __name__ == "__main__":
    app = ImageViewer()
    app.mainloop()
