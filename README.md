# Image Viewer Application

This repository contains a Python script that creates a simple image viewer application using the Tkinter library and the Python Imaging Library (PIL). The application allows users to open, save, and manipulate images, including rotation, cropping, adding text, adjusting brightness, contrast, and saturation, and applying hue adjustments.

## Installation

To run the application, you need to have Python installed on your system. You can download Python from the official website: https://www.python.org/downloads/

Once Python is installed, you can install the required libraries by running the following commands in your terminal or command prompt:

```
pip install pillow
pip install tk
```
or 

```
pip install -r requirements.txt
```

## Usage

To run the application, simply execute the `image_viewer.py` script. You can do this by running the following command in your terminal or command prompt:

```
python main.py
```

The application will open a GUI window where you can navigate through your files and perform various image manipulation operations.

## Features

- Open and save images in various formats (PNG, JPEG, GIF, BMP).
- Export images in different formats.
- Rotate images right or left.
- Crop images by selecting a region on the displayed image.
- Add text to images with customizable font size and position.
- Adjust brightness, contrast, and saturation of images.
- Apply hue adjustments to images.
- Undo and redo image manipulations.
- Zoom in and out on the displayed image.
- View keyboard shortcuts and about information.

## Keyboard Shortcuts

- `Ctrl+N`: Open an image.
- `Ctrl+S`: Save the current image.
- `Ctrl+E`: Export the current image.
- `Alt+F4`: Close the application.
- `Ctrl+Shift+R`: Rotate the image right.
- `Ctrl+R`: Rotate the image left.
- `Ctrl+T`: Add text to the image.
- `Ctrl+Z`: Undo the last image manipulation.
- `Ctrl+Y`: Redo the last undone image manipulation.
- `Ctrl++`: Zoom in on the displayed image.
- `Ctrl+-`: Zoom out on the displayed image.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.