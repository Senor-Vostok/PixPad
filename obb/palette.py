from PIL import Image
from PyQt5.Qt import QPixmap, QImage
from obb.colorhelper import blend_pixels
import math


def project_point_on_line(x, y, x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    if dx == 0 and dy == 0:
        return x1, y1
    t = ((x - x1) * dx + (y - y1) * dy) / (dx ** 2 + dy ** 2)
    t = max(0, min(1, t))
    px = x1 + t * dx
    py = y1 + t * dy
    return px, py


def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def interpolate_color(start_color, alpha):
    r, g, b, a = start_color
    a = alpha
    return r, g, b, a


def interpolate_alpha(base_alpha, dist, max_dist):
    fade = max(0, base_alpha - int((dist / max_dist) * 255))
    return fade


class Palette:
    def __init__(self, pattern_palette, name, chosen_color):
        self.palette = [[(255, 255, 255, 255), ((0, 0), (0, 255))], [(0, 0, 0, 255), ((0, 255), (255, 255))]]
        self.name = name
        self.color = chosen_color

    def colors_line(self, width):
        height = 20
        step = (255 * 6) // width
        line = Image.new("RGBA", (width, height))
        data = line.load()
        mode = [
            (0, step, 0, 0),
            (-step, 0, 0, 0),
            (0, 0, step, 0),
            (0, -step, 0, 0),
            (step, 0, 0, 0),
            (0, 0, -step, 0)
        ]
        for y in range(height):
            k_mode = 0
            color = (255, 0, 0, 255)
            for x in range(width):
                data[x, y] = color
                new_color = (
                    color[0] + mode[k_mode][0],
                    color[1] + mode[k_mode][1],
                    color[2] + mode[k_mode][2]
                )
                if any(spectre < 0 or spectre > 255 for spectre in new_color):
                    k_mode = (k_mode + 1) % len(mode)
                    new_color = (
                        color[0] + mode[k_mode][0],
                        color[1] + mode[k_mode][1],
                        color[2] + mode[k_mode][2]
                    )
                color = new_color
        return QPixmap(QImage(line.tobytes("raw", "RGBA"), width, height, QImage.Format_RGBA8888))

    def visibility_line(self, width):
        height = 20
        step = 255 // width
        line = Image.new("RGBA", (width, height))
        data = line.load()
        for x in range(width):
            for y in range(height):
                if (x // 16 + y // 16) % 2 == 0:
                    data[x, y] = (192, 192, 192, 255)
                else:
                    data[x, y] = (128, 128, 128, 255)
        for y in range(height):
            color = self.color[:3] + (255,)
            for x in range(width):
                data[x, y] = blend_pixels(color, data[x, y])
                color = (color[0], color[1], color[2], color[3] - step)
        return QPixmap(QImage(line.tobytes("raw", "RGBA"), width, height, QImage.Format_RGBA8888))

    def preview(self, width):
        height = 20
        line = Image.new("RGBA", (width, height))
        data = line.load()
        for x in range(width):
            for y in range(height):
                if (x // 16 + y // 16) % 2 == 0:
                    data[x, y] = blend_pixels(self.color, (192, 192, 192, 255))
                else:
                    data[x, y] = blend_pixels(self.color, (128, 128, 128, 255))
        return QPixmap(QImage(line.tobytes("raw", "RGBA"), width, height, QImage.Format_RGBA8888))

    def show_palette(self):
        size = 255
        palette_image = Image.new("RGBA", (size, size), self.color)
        data = palette_image.load()
        for color, points in self.palette:
            for i in range(len(points) - 1):
                x1, y1 = points[i]
                x2, y2 = points[i + 1]
                for y in range(size):
                    for x in range(size):
                        px, py = project_point_on_line(x, y, x1, y1, x2, y2)
                        line_dist = distance(x, y, px, py)
                        max_dist = size
                        if line_dist <= max_dist:
                            alpha = interpolate_alpha(color[3], line_dist, max_dist)
                            blended_color = blend_pixels(
                                interpolate_color(color, alpha), data[x, y]
                            )
                            data[x, y] = blended_color
        return QPixmap(QImage(palette_image.tobytes("raw", "RGBA"), size, size, QImage.Format_RGBA8888))
