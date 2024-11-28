class Brush:
    def __init__(self, pattern_path, geometry_path, color, size=1):
        self.pattern = pattern_path  # тут должен быть паттерн кисти(цвет, прозрачность), инициализация
        self.geometry = geometry_path  # тут должна быть геометрия кисти, инициализация !! её векторное построение !!
        self.ico = pattern_path  # тут должна быть иконка кисти, инициализация изображения в скейле 30 на 30 пикселей
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
            return self.ico  # Увеличенная иконка
        return self.ico
