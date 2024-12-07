from PIL import Image
from obb.layer import Layer
from obb.frame import Frame
from PyQt5.Qt import QImage, QPixmap
from obb.colorhelper import blend_pixels


class Canvas:
    def __init__(self, size, layers=(), current_frame=0, current_layer=0):
        self.layers = list()
        self.width, self.height = size
        self.background_color = (0, 0, 0, 0)
        self.light_gray = (128, 128, 128, 255)
        self.bright_gray = (192, 192, 192, 255)
        self.current_frame = current_frame
        self.current_layer = current_layer

        self.before_current_layer = Image.new("RGBA", (self.width, self.height), self.background_color)
        self.drawing_layer = Image.new("RGBA", (self.width, self.height), self.background_color)
        self.after_current_layer = Image.new("RGBA", (self.width, self.height), self.background_color)
        self.content = Image.new("RGBA", (self.width, self.height), self.background_color)

        self.before_data = self.before_current_layer.load()
        self.drawing_data = self.drawing_layer.load()
        self.after_data = self.after_current_layer.load()
        self.content_data = self.content.load()

        if layers:
            self.layers = layers
        else:
            first_frame = Frame(Image.new("RGBA", size, self.background_color))
            self.layers.append(Layer([first_frame]))

        self.brush_frame = Frame(Image.new("RGBA", size, self.background_color))  # Убрать потом
        self.update_canvas()
        self.history = [list(self.content.getdata())]

    def fill_pixels(self, pixels, display_brush=False):
        self.content.putdata(self.history[-1])
        have_after_layer = self.current_layer < len(self.layers) - 1
        have_before_layer = self.current_layer > 0
        for xoy, pixel in pixels:
            if pixel[3] == 255:
                self.drawing_data[xoy[0], xoy[1]] = pixel if not display_brush else self.drawing_data[xoy[0], xoy[1]]
                if have_after_layer and self.after_data[xoy[0], xoy[1]][3] != 255:
                    self.content_data[xoy[0], xoy[1]] = blend_pixels(self.after_data[xoy[0], xoy[1]], pixel)
                elif not have_after_layer:
                    self.content_data[xoy[0], xoy[1]] = pixel
            else:
                self.drawing_data[xoy[0], xoy[1]] = blend_pixels(pixel, self.drawing_data[xoy[0], xoy[1]]) if not display_brush else self.drawing_data[xoy[0], xoy[1]]
                if have_after_layer and have_before_layer:
                    self.content_data[xoy[0], xoy[1]] = blend_pixels(blend_pixels(pixel, self.drawing_data[xoy[0], xoy[1]]), self.before_data[xoy[0], xoy[1]])
                    self.content_data[xoy[0], xoy[1]] = blend_pixels(self.after_data[xoy[0], xoy[1]], self.content_data[xoy[0], xoy[1]])
                elif have_after_layer and not have_before_layer:
                    self.content_data[xoy[0], xoy[1]] = blend_pixels(blend_pixels(self.after_data[xoy[0], xoy[1]], pixel), self.content_data[xoy[0], xoy[1]])
                else:
                    self.content_data[xoy[0], xoy[1]] = blend_pixels(blend_pixels(pixel, self.drawing_data[xoy[0], xoy[1]]), self.content_data[xoy[0], xoy[1]])
        if not display_brush:
            self.history.append(list(self.content.getdata()))

    def update_canvas(self):
        self.content = Image.new("RGBA", (self.width, self.height), self.background_color)
        self.content_data = self.content.load()

        self.before_current_layer = Image.new("RGBA", (self.width, self.height), self.background_color)
        self.before_data = self.before_current_layer.load()
        for x in range(self.width):
            for y in range(self.height):
                if (x // 16 + y // 16) % 2 == 0:
                    self.before_data[x, y] = self.bright_gray
                else:
                    self.before_data[x, y] = self.light_gray
        if self.current_layer > 0:
            self.merge_layers(self.layers[:self.current_layer], self.before_data)

        self.drawing_layer = self.layers[self.current_layer]
        self.drawing_data = self.drawing_layer.get_content(self.current_frame).load()

        self.after_current_layer = Image.new("RGBA", (self.width, self.height), self.background_color)
        self.after_data = self.after_current_layer.load()
        if self.current_layer < len(self.layers) - 1:
            self.merge_layers(self.layers[self.current_layer + 1:], self.after_data)

        self.content = Image.new("RGBA", (self.width, self.height), self.background_color)
        self.content_data = self.content.load()
        for x in range(self.width):
            for y in range(self.height):
                self.content_data[x, y] = blend_pixels(blend_pixels(self.after_data[x, y], self.drawing_data[x, y]), self.before_data[x, y])

    def merge_layers(self, layers, output_data):
        for layer in layers:
            pixels = layer.get_content(self.current_frame).load()
            for x in range(self.width):
                for y in range(self.height):
                    if pixels[x, y][3] == 255:
                        output_data[x, y] = pixels[x, y]
                    else:
                        output_data[x, y] = blend_pixels(pixels[x, y], output_data[x, y])

    def get_content(self):
        return QPixmap(QImage(self.content.tobytes("raw", "RGBA"), self.width, self.height, QImage.Format_RGBA8888))
