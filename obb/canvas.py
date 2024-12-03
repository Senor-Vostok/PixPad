from PIL import Image
from obb.layer import Layer
from obb.frame import Frame
from PyQt5.Qt import QImage, QPixmap


def blend_pixels(pixel_top, pixel_bottom):
    r1, g1, b1, a1 = pixel_top
    r2, g2, b2, a2 = pixel_bottom
    alpha1 = a1 / 255.0
    alpha2 = a2 / 255.0
    alpha = alpha1 + alpha2 * (1 - alpha1)
    if alpha == 0:
        return 0, 0, 0, 0
    r = int((r1 * alpha1 + r2 * alpha2 * (1 - alpha1)) / alpha)
    g = int((g1 * alpha1 + g2 * alpha2 * (1 - alpha1)) / alpha)
    b = int((b1 * alpha1 + b2 * alpha2 * (1 - alpha1)) / alpha)
    a = int(alpha * 255)
    return r, g, b, a


class Canvas:
    def __init__(self, size, layers=(), current_frame=0, current_layer=0):
        self.layers = list()
        self.width, self.height = size
        self.background_color = (0, 0, 0, 0)
        self.light_gray = (128, 128, 128, 255)
        self.bright_gray = (192, 192, 192, 255)
        self.current_frame = current_frame
        self.current_layer = current_layer

        self.background_image = Image.new("RGBA", (self.width, self.height), self.background_color)
        pixels_o = self.background_image.load()
        for x in range(self.width):
            for y in range(self.height):
                if (x // 16 + y // 16) % 2 == 0:
                    pixels_o[x, y] = self.bright_gray
                else:
                    pixels_o[x, y] = self.light_gray

        self.before_current_layer = None
        self.after_current_layer = None

        if layers:
            self.layers = layers
        else:
            first_frame = Frame(Image.new("RGBA", size, self.background_color))
            self.layers.append(Layer([first_frame]))
        self.brush_frame = Frame(Image.new("RGBA", size, self.background_color))

    def get_content(self):
        pixels_o = list(self.background_image.getdata())
        for layer in self.layers:  # Надо оптимизировать
            if not layer.is_active:
                continue
            frame = layer.get_content(self.current_frame)
            pixels = list(frame.getdata())
            for i, pixel in enumerate(pixels_o):
                if layer.visibility < 1 or pixels[i][3] < 255:
                    pixels_o[i] = blend_pixels(pixels[i], pixel)
                else:
                    pixels_o[i] = pixels[i]
        pix_brush = list(self.brush_frame.image.getdata())
        for i, pixel in enumerate(pixels_o):  # Может вообще перевести на отдельный Layer
            if pix_brush[i][3] < 255:
                pixels_o[i] = blend_pixels(pix_brush[i], pixel)
            else:
                pixels_o[i] = pix_brush[i]
        final = Image.new("RGBA", (self.width, self.height), self.background_color)
        final.putdata(pixels_o)
        data = final.tobytes("raw", "RGBA")
        del self.brush_frame
        self.brush_frame = Frame(Image.new("RGBA", (self.width, self.height), self.background_color))
        return QPixmap(QImage(data, self.width, self.height, QImage.Format_RGBA8888))
