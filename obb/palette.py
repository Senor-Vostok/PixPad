from PIL import Image
from PyQt5.Qt import QPixmap, QImage


class Palette:
    def __init__(self, pattern_palette, name, chosen_color):
        self.palette = pattern_palette
        self.name = name
        self.color = chosen_color

    def show_palette(self):
        palette_image = Image.new("RGB", (255, 255))
        white = (255, 255, 255)
        gray = (40, 40, 40)
        black = (0, 0, 0)
        data = palette_image.load()
        for y in range(255):
            for x in range(255):
                ratio_x = x/255
                ratio_y = y/255
                r = int((1 - ratio_y) * (1 - ratio_x) * white[0] + ratio_y * (1 - ratio_x) *
                        gray[0] + ratio_x * (1 - ratio_y) * self.color[0] + ratio_y * ratio_x * black[0])
                g = int((1 - ratio_y) * (1 - ratio_x) * white[1] + ratio_y * (1 - ratio_x) * gray[1] + ratio_x * (1 - ratio_y) *
                        self.color[1] + ratio_y * ratio_x * black[1])
                b = int((1 - ratio_y) * (1 - ratio_x) * white[2] + ratio_y * (1 - ratio_x) * gray[2] + ratio_x * (1 - ratio_y) *
                        self.color[2] + ratio_y * ratio_x * black[2])
                data[x, y] = (r, g, b)
        return QPixmap(QImage(palette_image.tobytes("raw", "RGB"), 255, 255, QImage.Format_RGB888))
