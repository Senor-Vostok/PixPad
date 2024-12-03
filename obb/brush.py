from PyQt5.Qt import QImage
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QCursor, QPixmap
from PIL import Image


class Brush:
    def __init__(self, pattern_path, color=(0, 128, 255, 255), size_coef=1):
        self.pattern_path = 'C:/Users/alber/PixPad/data/brushes/test_brush/Vector.svg'  # Пока так
        self.ico = QPixmap(QImage(pattern_path))
        self.send_pack = list()
        self.cx = 0.00000
        self.cy = 0.00000
        self.rx = 0.00000
        self.ry = 0.00000
        self.geometry = [[[0, 0]],  # 1
                         [[0, 0], [1, 0], [0, 1], [1, 1]],  # 2
                         [[0, 0], [1, 0], [0, 1], [-1, 0], [0, -1]],  # 3
                         ]
        self.color = color

        self.size = size_coef

    def get_parametrs(self):
        with open(self.pattern_path, mode='rt') as f:
            for i in f.readlines():
                if 'cx' in i and "inkscape" not in i:
                    i = i.replace('cx="', '')
                    i = i.replace('"', '')
                    i = i.split()
                    print(i)
                    self.cx = float(i[0])
                if 'cy' in i and "inkscape" not in i:
                    i = i.replace('cy="', '')
                    i = i.replace('"', '')
                    i = i.split()
                    print(i)
                    self.cy = float(i[0])
                if 'rx' in i and "inkscape" not in i:
                    i = i.replace('rx="', '')
                    i = i.replace('"', '')
                    i = i.split()
                    print(i)
                    self.rx = float(i[0])
                if 'ry' in i and "inkscape" not in i:
                    i = i.replace('ry="', '')
                    i = i.replace('"', '')
                    i = i.split()
                    print(i)
                    self.ry = float(i[0])

    def resize(self, new_size):  # прописать логику увеличения кисти
        pass

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
        self.get_parametrs()
        self.send_pack.clear()
        image_data = list(canvas.brush_frame.image.getdata())
        image_width, image_height = canvas.brush_frame.image.size
        for index in range(len(image_data)):
            x = index % image_width
            y = index // image_width
            cx = xoy.x() // k
            cy = xoy.y() // k
            if (cx, cy) == (x, y) or (cx - self.rx < x < cx + self.rx and cy - self.ry < y < cy + self.ry):
                image_data[index] = self.color # пока для отображения оставил
                # вот передача пикселей self.send_pack.append(index)
        canvas.brush_frame.image.putdata(image_data)
        return self.send_pack

