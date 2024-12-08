from PyQt5.Qt import QImage
from math import sqrt
from PyQt5.QtGui import QPixmap
from obb.Brush.simple_brush import SimpleBrush


class Brush(SimpleBrush):
    def __init__(self, pattern_path, color=(0, 128, 255, 255), size_coef=1):
        self.pattern_path = 'data/brushes/test_brush/Vector.svg'
        self.ico = QPixmap(QImage(pattern_path))
        self.send_pack = list()
        self.cx = 0.00000
        self.cy = 0.00000
        self.rx = 0.00000
        self.ry = 0.00000
        self.geometry = [[0, 0], [1, 0], [0, 1], [-1, 0], [0, -1]]
        self.figure = 'BOB'
        self.color = color

        self.size = size_coef
        self.init_brush()

    def init_brush(self):
        self.get_parametrs()
        self.resize(1)

    def get_parametrs(self):
        with open(self.pattern_path, mode='rt') as f:
            for i in f.readlines():
                if 'cx' in i and "inkscape" not in i:
                    i = i.replace('cx="', '')
                    i = i.replace('"', '')
                    i = i.split()
                    self.cx = float(i[0])
                if 'cy' in i and "inkscape" not in i:
                    i = i.replace('cy="', '')
                    i = i.replace('"', '')
                    i = i.split()
                    self.cy = float(i[0])
                if 'rx' in i and "inkscape" not in i:
                    i = i.replace('rx="', '')
                    i = i.replace('"', '')
                    i = i.split()
                    self.rx = float(i[0])
                if 'ry' in i and "inkscape" not in i:
                    i = i.replace('ry="', '')
                    i = i.replace('"', '')
                    i = i.split()
                    self.ry = float(i[0])

    def resize(self, new_size=1):
        if self.rx + new_size > 64:
            return
        scale = new_size / self.size if self.size != 0 else 1
        self.size = new_size
        if self.size <= 3:
            self.geometry = [[0, 0], [1, 0], [0, 1], [1, 1]] if self.size == 2 else [[0, 0]]
            self.geometry = [[0, 0], [1, 0], [0, 1], [1, 1]] if self.size == 3 else self.geometry
            return
        self.rx = int(self.rx * scale)
        self.ry = int(self.ry * scale)
        cells = []
        for x in range(round(-self.rx), round(self.rx + 1)):
            for y in range(round(-self.ry), round(self.ry + 1)):
                if sqrt((x ** 2) / round(self.rx) ** 2 + (y ** 2) / round(self.ry) ** 2) <= 1:
                    cells.append((x, y))
        self.geometry = cells

    def recolor(self, new_color):  # прописать логику изменения цвета
        self.color = new_color

    def draw(self, canvas, current_frame, xoy, k):
        pass

    def get_ico(self, current_size=None):
        if current_size:
            b = self.ico.scaled(current_size[0], current_size[1])
            return b  # Увеличенная иконка
        return self.ico

    def brush(self, canvas, xoy, k, brushing):
        cx = xoy.x() // k
        cy = xoy.y() // k
        canvas.fill_pixels([[(cx + i[0], cy + i[1]), self.color] for i in self.geometry if 0 <= (cx + i[0]) < canvas.width and 0 <= (cy + i[1]) < canvas.height], brushing)