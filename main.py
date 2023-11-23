import tkinter as tk
from tkinter import filedialog
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

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_image)
        file_menu.add_command(label="Save", command=self.save_image)
        file_menu.add_command(label="Exit", command=self.quit)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Rotate Right", command=self.rotate_right)
        edit_menu.add_command(label="Rotate Left", command=self.rotate_left)

        self.rotation_count = 0
        self.original_image = None

        #Keyboard shortcuts
        self.bind_all("<Control-o>", lambda event: self.open_image())
        self.bind_all("<Control-s>", lambda event: self.save_image())
        self.bind_all("<Control-q>", lambda event: self.quit())
        self.bind_all("<Control-r>", lambda event: self.rotate_right())
        self.bind_all("<Control-l>", lambda event: self.rotate_left())


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

if __name__ == "__main__":
    app = ImageViewer()
    app.mainloop()
