from PyQt5.QtGui import QPixmap, QImage
from obb.tools.base import BaseTool


class SimpleBrush(BaseTool):
    def __init__(self, pattern_path, vector_path, color=(0, 128, 255, 255), size_coef=1):
        super().__init__(vector_path.split('/')[-1], color, size_coef)
        self.pattern_path = vector_path
        self.ico = QPixmap(QImage(pattern_path))
        self.send_pack = []
        self.cx = 0.0
        self.cy = 0.0
        self.base_size = size_coef
        self.base_rx = 0.0
        self.base_ry = 0.0
        self.geometry = [[0, 0]]
        self.size = size_coef

    def resize(self, new_size) -> None:
        self.size = new_size

    def get_ico(self, current_size=None):
        if current_size:
            return self.ico.scaled(current_size[0], current_size[1])
        return self.ico
