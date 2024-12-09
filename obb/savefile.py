from PIL import Image


class PixelEditorSaver:
    def __init__(self, width, height, background_color, content):
        self.width = width
        self.height = height
        self.background_color = background_color
        self.content = content

    def save_as_png(self, filename):
        transparent_image = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        transparent_data = transparent_image.load()
        content_data = self.content.load()
        for x in range(self.width):
            for y in range(self.height):
                pixel = content_data[x, y]
                if pixel[:3] == self.background_color[:3]:
                    transparent_data[x, y] = (0, 0, 0, 0)
                else:
                    transparent_data[x, y] = pixel
        transparent_image.save(filename, "PNG")

