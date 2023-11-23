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
        file_menu.add_command(label="Exit", command=self.quit)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
        if file_path:
            image = Image.open(file_path)
            photo = ImageTk.PhotoImage(image)

            self.image_label.config(image=photo)
            self.image_label.image = photo

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
        if file_path:
            image = Image.open(file_path)
            self.original_image = image.copy()  # Store the original image for editing
            photo = ImageTk.PhotoImage(image)

            self.image_label.config(image=photo)
            self.image_label.image = photo

    def rotate_image(self):
        if hasattr(self, 'original_image'):
            rotated_image = self.original_image.rotate(90)
            photo = ImageTk.PhotoImage(rotated_image)

            self.image_label.config(image=photo)
            self.image_label.image = photo

if __name__ == "__main__":
    app = ImageViewer()

    rotate_button = tk.Button(app, text="Rotate", command=app.rotate_image)
    rotate_button.pack()

    app.mainloop()
