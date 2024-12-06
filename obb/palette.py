#from PIL import Image

class Palette:
    def __init__(self, pattern_palette, name, chosen_color):
        self.palette = pattern_palette  # Инструкции построения палитры
        self.name = name
        self.color = chosen_color

    def show_palette(self, color):  # построение палитры при выбранном цвете, используя инструкции
        #palette_image = Image.new("RGB", (255, 255)) для построения изображения палитры (?)
        #основное построение палитры

        white = (255, 255, 255)
        gray = (40, 40, 40)
        black = (0, 0, 0)

        for y in range(255):
            for x in range(255):
                ratio_x = x/255
                ratio_y = y/255

                r = int((1 - ratio_y) * (1 - ratio_x) * white[0] + ratio_y * (1 - ratio_x) *
                        gray[0] + ratio_x * (1 - ratio_y) * color[0] + ratio_y * ratio_x * black[0])
                g = int((1 - ratio_y) * (1 - ratio_x) * white[1] + ratio_y * (1 - ratio_x) * gray[1] + ratio_x * (1 - ratio_y) *
                        color[1] + ratio_y * ratio_x * black[1])
                b = int((1 - ratio_y) * (1 - ratio_x) * white[2] + ratio_y * (1 - ratio_x) * gray[2] + ratio_x * (1 - ratio_y) *
                        color[2] + ratio_y * ratio_x * black[2])

                #palette_image.putpixel((x, y), (r, g, b))

        #return palette_image