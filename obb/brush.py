from PyQt5.Qt import QImage
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QCursor, QPixmap
from PIL import Image


class Brush:
    def __init__(self, pattern_path, color=(0, 128, 255, 255), size_coef=1):
        self.ico = QPixmap(QImage(pattern_path))
        self.color = color
        self.size = size_coef

    def resize(self, new_size):  # прописать логику увеличения кисти
        self.size = new_size

    def recolor(self, new_color):  # прописать логику изменения цвета
        self.color = new_color

    def draw(self, canvas, current_frame, xoy, k):
        pass

    def get_ico(self, current_size=None):
        if current_size:
            b = self.ico.scaled(current_size[0], current_size[1])
            return b  # Увеличенная иконка
        return self.ico

    def display_brush(self, canvas, xoy, k):
        image_data = list(canvas.brush_frame.image.getdata())
        image_width, image_height = canvas.brush_frame.image.size
        for index in range(len(image_data)):
            x = index % image_width
            y = index // image_width
            if (xoy.x() // k, xoy.y() // k) == (x, y):
                image_data[index] = self.color
        canvas.brush_frame.image.putdata(image_data)
