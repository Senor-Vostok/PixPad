from PIL import Image
import os
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

if __name__ == "__main__":
    width, height = 128, 128
    background_color = (255, 255, 255, 255)

    content = Image.new("RGBA", (width, height), background_color)
    content_data = content.load()
    for x in range(0, width, 2):
        for y in range(0, height, 2):
            content_data[x, y] = (255, 0, 0, 255)

    saver = PixelEditorSaver(width, height, background_color, content)
    saver.save_as_png("a.png")