from PyQt5.Qt import QImage
from PyQt5.Qt import QPixmap
from PyQt5.QtWidgets import QPushButton
class Brush:
    def __init__(self, pattern_path, geometry_path, color, size=1):
        self.pattern = pattern_path  # тут должен быть паттерн кисти(цвет, прозрачность), инициализация
        self.geometry = geometry_path  # тут должна быть геометрия кисти, инициализация !! её векторное построение !!
        # self.ico = QImage(pattern_path)   # тут должна быть иконка кисти, инициализация изображения в скейле 30 на 30 пикселей
        self.ico = QPixmap(QImage(pattern_path))
        self.color = color
        self.size = size

    def resize(self, new_size):  # прописать логику увеличения кисти
        self.size = new_size

    def draw(self, space, xoy):  # прописать логику рисования
        pass

    def recolor(self, new_color):  # прописать логику изменения цвета
        self.color = new_color

    def get_ico(self, current_size=None):
        if current_size:
            b = self.ico.scaled(current_size[0], current_size[1])
            return b # Увеличенная иконка
        return self.ico
