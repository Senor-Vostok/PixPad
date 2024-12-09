from PyQt5.Qt import QImage
from math import sqrt
from PyQt5.QtGui import QPixmap
from obb.Brush.simple_brush import SimpleBrush


class Brush(SimpleBrush):
    def __init__(self, pattern_path, vector_path):
        super().__init__(pattern_path, vector_path)
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
                    self.base_rx = float(i[0])
                if 'ry' in i and "inkscape" not in i:
                    i = i.replace('ry="', '')
                    i = i.replace('"', '')
                    i = i.split()
                    self.base_ry = float(i[0])

    def resize(self, new_size=1):
        scale = new_size / self.base_size
        self.size = new_size
        rx = float(self.base_rx * scale)  # Масштабируем базовый радиус rx
        ry = float(self.base_ry * scale)
        if self.size <= 3:
            self.geometry = [[0, 0], [1, 0], [0, 1], [1, 1]] if self.size == 2 else [[0, 0]]
            self.geometry = [[0, 0], [1, 0], [0, 1], [-1, 0], [0, -1]] if self.size == 3 else self.geometry
            return
        cells = []
        for x in range(round(-rx), round(rx + 1)):
            for y in range(round(-ry), round(ry + 1)):
                if sqrt((x ** 2) / round(rx) ** 2 + (y ** 2) / round(ry) ** 2) <= 1:
                    cells.append((x, y))
        self.geometry = cells

    def brush(self, canvas, xoy, k, brushing):
        cx = xoy.x() // k
        cy = xoy.y() // k
        canvas.fill_pixels([[(cx + i[0], cy + i[1]), self.color] for i in self.geometry if 0 <= (cx + i[0]) < canvas.width and 0 <= (cy + i[1]) < canvas.height], brushing)