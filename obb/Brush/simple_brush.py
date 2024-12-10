from PyQt5.QtGui import QPixmap, QImage


class SimpleBrush:
    def __init__(self, pattern_path, vector_path, color=(0, 128, 255, 255), size_coef=1):
        self.pattern_path = vector_path
        self.ico = QPixmap(QImage(pattern_path))
        self.send_pack = list()
        self.cx = 0.00000
        self.cy = 0.00000
        self.base_size = size_coef
        self.base_rx = 0.000
        self.base_ry = 0.000
        self.geometry = [[0, 0], [1, 0], [0, 1], [-1, 0], [0, -1]]
        self.figure = 'BOB'
        self.color = color

        self.size = size_coef

    def resize(self, new_size) -> None: ...

    def get_ico(self, current_size=None):
        if current_size:
            b = self.ico.scaled(current_size[0], current_size[1])
            return b
        return self.ico

    def brush(self, canvas, xoy, k, brushing) -> None: ...
