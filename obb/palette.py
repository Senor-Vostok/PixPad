from PIL import Image
from PyQt5.Qt import QPixmap, QImage
from obb.colorhelper import *


class Palette:
    def __init__(self, pattern_palette, name, chosen_color):
        self.palette = [[(255, 255, 255, 255), ((0, 0), (0, 255))], [(0, 0, 0, 255), ((0, 255), (255, 255))]]
        self.name = name
        self.color = chosen_color
        self.contrast_color = chosen_color
        self.line_colors = Image.new("RGBA", (255, 10))
        self.data_colors = self.line_colors.load()
        self.colors_line(255)
        self.old_xoy = (0, 0)

    def _generate_checker_pattern(self, width, height, base_color):
        pattern = Image.new("RGBA", (width, height))
        data = pattern.load()
        light_gray = (192, 192, 192, 255)
        dark_gray = (128, 128, 128, 255)
        for x in range(width):
            for y in range(height):
                data[x, y] = blend_pixels(
                    base_color, light_gray if (x // 16 + y // 16) % 2 == 0 else dark_gray
                )
        return pattern

    def preview(self, width=255):
        height = 40
        line = self._generate_checker_pattern(width, height, self.color)
        return QPixmap(QImage(line.tobytes("raw", "RGBA"), width, height, QImage.Format_RGBA8888))

    def colors_line(self, width=255, xoy=None):
        height = 20
        step = (255 * 6) // width
        self.line_colors = Image.new("RGBA", (width, height))
        self.data_colors = self.line_colors.load()
        mode = [
            (0, step, 0, 0), (-step, 0, 0, 0), (0, 0, step, 0),
            (0, -step, 0, 0), (step, 0, 0, 0), (0, 0, -step, 0)
        ]
        for y in range(height):
            k_mode = 0
            color = [255, 0, 0, 255]
            for x in range(width):
                self.data_colors[x, y] = tuple(color)
                new_color = [
                    color[i] + mode[k_mode][i] for i in range(4)
                ]
                if any(spectre < 0 or spectre > 255 for spectre in new_color):
                    k_mode = (k_mode + 1) % len(mode)
                    new_color = [
                        color[i] + mode[k_mode][i] for i in range(4)
                    ]
                color = new_color
        x, y = find_closest_color(
            self.data_colors, width, height, self.color[:3] + (255,)
        ) if not xoy else xoy
        self.contrast_color = self.data_colors[x, y]
        draw_border_circle(self.data_colors, width, height, (x, height // 2))
        return QPixmap(QImage(self.line_colors.tobytes("raw", "RGBA"), width, height, QImage.Format_RGBA8888))

    def visibility_line(self, width=255, xoy=None):
        height = 20
        step = 255 // width
        line = self._generate_checker_pattern(width, height, (0, 0, 0, 255))
        data = line.load()
        for x in range(width):
            for y in range(height):
                if (x // 16 + y // 16) % 2 == 0:
                    data[x, y] = (192, 192, 192, 255)
                else:
                    data[x, y] = (128, 128, 128, 255)
        for y in range(height):
            color = list(self.color[:3]) + [255]
            for x in range(width):
                data[x, y] = blend_pixels(tuple(color), data[x, y])
                color[3] -= step

        if xoy:
            self.color = self.color[:3] + (255 - xoy[0],)
        draw_border_circle(data, width, height, (255 - self.color[3], height // 2))
        return QPixmap(QImage(line.tobytes("raw", "RGBA"), width, height, QImage.Format_RGBA8888))

    def show_palette(self, xoy=None, changed_contrast=False):
        size = 255
        palette_image = Image.new("RGBA", (size, size), self.contrast_color)
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

        if not changed_contrast:
            x, y = find_closest_color(
                data, size, size, self.color[:3] + (255,)
            ) if not xoy else xoy
            self.old_xoy = (x, y)
        else:
            x, y = self.old_xoy

        self.color = data[x, y][:3] + (self.color[3],)
        draw_border_circle(data, size, size, (x, y))
        return QPixmap(QImage(palette_image.tobytes("raw", "RGBA"), size, size, QImage.Format_RGBA8888))
