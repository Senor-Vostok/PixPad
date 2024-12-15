from PIL import Image


class PixelEditorSaver:
    def __init__(self, width, height, background_color, content, canvas):
        self.width = width
        self.height = height
        self.background_color = background_color
        self.content = content
        self.canvas = canvas

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

    def save_as_jpeg(self, filename):
        white_background = Image.new("RGB", (self.width, self.height), (255, 255, 255))
        white_background.paste(self.content, (0, 0), self.content)
        white_background.save(filename, "JPEG")

    def save_as_gif(self, filename):
        count_f = len(self.canvas.layers[0].frames)
        current_frame = self.canvas.current_frame
        frames = []


        for i in range(count_f):
            self.canvas.current_frame = i
            img = self.canvas.get_raw()
            rgb_img = img.convert("RGB")

            indexed_img = img.convert("P", palette=Image.ADAPTIVE, colors=256)
            frames.append(indexed_img)

        self.canvas.current_frame = current_frame

        if frames:
            frames[0].save(filename, save_all=True, append_images=frames[1:], duration=100, loop=0)

