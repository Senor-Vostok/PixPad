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
        self.update_canvas()
        self.brush_history = [()]
        self.history = [[tuple(self.before_current_layer.getdata()),
                         tuple(self.drawing_layer.getdata()),
                         tuple(self.after_current_layer.getdata())]]

    def fill_pixels(self, pixels, display_brush=False, erase=False):
        if not self.layers[self.current_layer].is_active:
            return
        if not display_brush:
            self.brush_history.clear()
        if display_brush:
            if self.brush_history:
                old_pixels = self.brush_history[-1]
                for xoy, pixel in old_pixels:
                    self.content_data[xoy[0], xoy[1]] = pixel
                self.brush_history = self.brush_history[-1:]
            self.brush_history.append([(xoy, self.content_data[xoy[0], xoy[1]]) for xoy, pixel in pixels])
        for xoy, pixel in pixels:
            if not erase:
                self.drawing_data[xoy[0], xoy[1]] = blend_pixels(pixel, self.drawing_data[xoy[0], xoy[1]]) if not display_brush else self.drawing_data[xoy[0], xoy[1]]
                self.content_data[xoy[0], xoy[1]] = blend_pixels(self.after_data[xoy[0], xoy[1]], blend_pixels(pixel, blend_pixels(self.drawing_data[xoy[0], xoy[1]], self.before_data[xoy[0], xoy[1]])))
            else:
                self.drawing_data[xoy[0], xoy[1]] = (0, 0, 0, 0) if not display_brush else self.drawing_data[xoy[0], xoy[1]]
                self.content_data[xoy[0], xoy[1]] = blend_pixels(self.after_data[xoy[0], xoy[1]], blend_pixels((0, 0, 0, 0), self.before_data[xoy[0], xoy[1]]))

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

        if self.layers[self.current_layer].is_active:
            self.drawing_layer = self.layers[self.current_layer].get_content(self.current_frame)
        self.drawing_data = self.drawing_layer.load()

        self.after_current_layer = Image.new("RGBA", (self.width, self.height), self.background_color)
        self.after_data = self.after_current_layer.load()
        if self.current_layer < len(self.layers) - 1:
            self.merge_layers(self.layers[self.current_layer + 1:], self.after_data)

        for x in range(self.width):
            for y in range(self.height):
                self.content_data[x, y] = blend_pixels(blend_pixels(self.after_data[x, y], self.drawing_data[x, y]), self.before_data[x, y])

    def merge_layers(self, layers, output_data):
        for layer in layers:
            if layer.is_active:
                pixels = layer.get_content(self.current_frame).load()
                for x in range(self.width):
                    for y in range(self.height):
                        if pixels[x, y][3] == 255:
                            output_data[x, y] = pixels[x, y]
                        else:
                            output_data[x, y] = blend_pixels(pixels[x, y], output_data[x, y])

    def get_content(self):
        return QPixmap(QImage(self.content.tobytes("raw", "RGBA"), self.width, self.height, QImage.Format_RGBA8888))

    def add_frame(self):
        for layer in self.layers:
            layer.frames.append(Frame(Image.new("RGBA", (self.width, self.height), self.background_color)))

    def add_layout(self):
        frames = list()
        for i in range(len(self.layers[0].frames)):
            frames.append(Frame(Image.new("RGBA", (self.width, self.height), self.background_color)))
        self.layers.append(Layer(frames))

    def get_raw(self):
        content = Image.new("RGBA", (self.width, self.height), self.background_color)
        content_data = content.load()
        before_current_layer = Image.new("RGBA", (self.width, self.height), self.background_color)
        before_data = before_current_layer.load()
        if self.current_layer > 0:
            self.merge_layers(self.layers[:self.current_layer], before_data)

        if self.layers[self.current_layer].is_active:
            drawing_layer = self.layers[self.current_layer]
        drawing_data = drawing_layer.get_content(self.current_frame).load()

        after_current_layer = Image.new("RGBA", (self.width, self.height), self.background_color)
        after_data = after_current_layer.load()
        if self.current_layer < len(self.layers) - 1:
            self.merge_layers(self.layers[self.current_layer + 1:], after_data)

        for x in range(self.width):
            for y in range(self.height):
                content_data[x, y] = blend_pixels(blend_pixels(after_data[x, y], drawing_data[x, y]), before_data[x, y])
        return content
