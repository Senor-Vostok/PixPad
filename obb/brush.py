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

    def get_ico(self, current_size=None):
        if current_size:
            b = self.ico.scaled(current_size[0], current_size[1])
            return b  # Увеличенная иконка
        return self.ico

    def display_brush(self, canvas, xoy):
        image_data = list(canvas.brush_frame.image.getdata())
        image_width, image_height = canvas.brush_frame.image.size
        for index in range(len(image_data)):
            x = index % image_width
            y = index // image_width
            if xoy == (x, y):
                image_data[index] = self.color
            rad = abs(xoy.x() - self.size) // 2
            x_up, x_down = xoy.x() + rad, xoy.x() - rad
            y_up, y_down = xoy.y() + rad, xoy.y() - rad
            print(image_data[index], self.color)
            if int(x_down) < int(x) < int(x_up) and int(y_down) < int(y) < int(y_up):
                image_data[index] = self.color
        canvas.brush_frame.image.putdata(image_data)
