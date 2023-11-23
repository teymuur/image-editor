import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw

class ImageViewer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Image Viewer")
        self.geometry("800x600")

        self.canvas = tk.Canvas(self)
        self.canvas.pack(expand="true")

        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        # file menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_image, accelerator="Ctrl+N")
        file_menu.add_command(label="Save", command=self.save_image, accelerator="Ctrl+S")
        file_menu.add_command(label="Exit", command=self.quit, accelerator="Alt+F4")

        # edit menu
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Crop", command=self.start_crop, accelerator="F2")
        edit_menu.add_command(label="Rotate Right", command=self.rotate_right, accelerator="Ctrl+Shift+R")
        edit_menu.add_command(label="Rotate Left", command=self.rotate_left, accelerator="Ctrl+R")

        edit_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        
        # help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Keyboard Shortcuts", command=self.show_shortcuts)
        
        self.rotation_count = 0
        self.original_image = None
        self.image_history = []
        self.history_index = -1

        # Keyboard shortcuts
        self.bind_all("<Control-n>", self.open_image)
        self.bind_all("Control-KeyPress>", self.start_crop)
        self.bind_all("<Control-s>", self.save_image)
        self.bind_all("<Alt-F4>", self.quit)
        self.bind_all("<Control-Shift-R>", self.rotate_right)
        self.bind_all("<Control-R>", self.rotate_left)
        self.bind_all("<Control-z>", self.undo)
        self.bind_all("<Control-y>", self.redo)

        # cropping adjustments
        self.cropping = False
        self.crop_start = (0, 0)
        self.crop_rectangle = None

    def open_image(self, event=None):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
        if file_path:
            image = Image.open(file_path)
            self.original_image = image.copy()
            self.rotation_count = 0
            self.update_image()
            self.save_to_history()

    def update_image(self):
        if hasattr(self, 'original_image'):
            rotated_image = self.original_image.rotate(90 * self.rotation_count)
            photo = ImageTk.PhotoImage(rotated_image)

            self.canvas.config(width=photo.width(), height=photo.height())
            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvas.photo = photo

    def rotate_right(self, event=None):
        self.rotation_count -= 1
        self.update_image()
        self.save_to_history()

    def rotate_left(self, event=None):
        self.rotation_count += 1
        self.update_image()
        self.save_to_history()

    def save_image(self, event=None):
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
                self.save_to_history()

    def show_shortcuts(self):
        shortcuts_info = (
            "Ctrl+N - Open Image\n"
            "Ctrl+S - Save Image\n"
            "Alt+F4 - Exit\n"
            "Ctrl+Shift+R - Rotate Right\n"
            "Ctrl+R - Rotate Left\n"
            "F2 Crop\n"
            "Ctrl+Z - Undo\n"
            "Ctrl+Y - Redo"
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

    def start_crop(self):
        if hasattr(self, 'original_image'):
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

            rotated_image = self.original_image.rotate(90 * self.rotation_count)
            cropped_image = rotated_image.crop((x, y, x1, y1))
            self.original_image = cropped_image
            self.cropping = False
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<ButtonRelease-1>")
            self.save_to_history()
            self.update_image()

    def save_to_history(self):
        if self.original_image is not None:
            # If we are undoing, discard any redo history beyond the current position
            if self.history_index < len(self.image_history) - 1:
                self.image_history = self.image_history[:self.history_index + 1]

            # Save a copy of the current image
            self.image_history.append(self.original_image.copy())
            self.history_index = len(self.image_history) - 1

    def undo(self, event=None):
        if self.history_index > 0:
            self.history_index -= 1
            self.original_image = self.image_history[self.history_index].rotate(-90 * self.rotation_count)
            self.update_image()


    def redo(self, event=None):
        if self.history_index < len(self.image_history) - 1:
            self.history_index += 1
            self.original_image = self.image_history[self.history_index].rotate(-90 * self.rotation_count)
            self.update_image()



if __name__ == "__main__":
    app = ImageViewer()
    app.mainloop()
