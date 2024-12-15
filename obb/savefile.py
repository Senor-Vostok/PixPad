from PIL import Image


class PixelEditorSaver:
    def __init__(self, width, height, background_color, content, canvas):
        self.width = width
        self.height = height
        self.background_color = background_color
        self.content = content
        self.canvas = canvas

    def save_as_png(self, filename):
        try:
            count_f = len(self.canvas.layers[0].frames)
            content = Image.new("RGBA", (self.width * count_f, self.height))
            current_frame = self.canvas.current_frame
            data_content = content.load()
            for i in range(count_f):
                self.canvas.current_frame = i
                img = self.canvas.get_raw()
                img_data = img.load()
                for x in range(self.width):
                    for y in range(self.height):
                        data_content[x + i * self.width, y] = img_data[x, y]
            self.canvas.current_frame = current_frame
            content.save(filename, "PNG")
        except Exception as e:
            print(e)

    def save_as_jpeg(self, filename):
        white_background = Image.new("RGB", (self.width, self.height))
        white_background.paste(self.content, (0, 0), self.content)
        white_background.save(filename, "JPEG")

    def save_as_gif(self, filename, duration=100):
        count_f = len(self.canvas.layers[0].frames)
        current_frame = self.canvas.current_frame
        frames = []
        for i in range(count_f):
            self.canvas.current_frame = i
            img = self.canvas.get_raw()
            indexed_img = img.convert("RGBA", palette=Image.ADAPTIVE, colors=256)
            frames.append(indexed_img)
        self.canvas.current_frame = current_frame
        frames[0].save(filename, save_all=True, append_images=frames[1:], duration=duration, loop=0)

