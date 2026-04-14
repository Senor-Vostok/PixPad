from PIL import Image
from PyQt5.Qt import QImage, QPixmap
from obb.layer import Layer
from obb.frame import Frame
from obb.colorhelper import blend_pixels, invert_pixel


class Canvas:
    def __init__(self, size, layers=(), current_frame=0, current_layer=0):
        self.layers = list(layers) if layers else []
        self.width, self.height = size
        self.background_color = (0, 0, 0, 0)
        self.light_gray = (128, 128, 128, 255)
        self.bright_gray = (192, 192, 192, 255)
        self.current_frame = current_frame
        self.current_layer = current_layer
        if not self.layers:
            first_frame = Frame(Image.new('RGBA', size, self.background_color))
            self.layers.append(Layer([first_frame]))

        self.content = Image.new('RGBA', (self.width, self.height), self.background_color)
        self.action_history = []
        self.in_action = False
        self.preview_images = {}
        self.preview_border_points = []
        self.overlay_border_points = []
        self.update_canvas()

    def _new_image(self):
        return Image.new('RGBA', (self.width, self.height), self.background_color)

    def get_current_image(self):
        return self.layers[self.current_layer].get_content(self.current_frame)

    def get_layer_image(self, layer_index, frame_number=None):
        frame_number = self.current_frame if frame_number is None else frame_number
        return self.layers[layer_index].get_content(frame_number)

    def set_current_image(self, image, update=True):
        self.layers[self.current_layer].set_content(self.current_frame, image)
        if update:
            self.update_canvas()

    def set_layer_image(self, layer_index, image, frame_number=None, update=True):
        frame_number = self.current_frame if frame_number is None else frame_number
        self.layers[layer_index].set_content(frame_number, image)
        if update:
            self.update_canvas()

    def begin_action(self, layer_indices=None, frame_number=None):
        if self.in_action:
            return
        frame_number = self.current_frame if frame_number is None else frame_number
        if layer_indices is None:
            layer_indices = [self.current_layer]
        entry = {
            'frame': frame_number,
            'current_layer': self.current_layer,
            'layers': {index: self.layers[index].get_content(frame_number).copy() for index in layer_indices},
        }
        self.action_history.append(entry)
        self.in_action = True

    def cancel_action(self):
        if self.in_action and self.action_history:
            self.action_history.pop()
        self.in_action = False
        self.clear_preview(update=False)
        self.update_canvas()

    def end_action(self):
        self.in_action = False
        self.clear_preview(update=False)
        self.update_canvas()

    def undo(self):
        if not self.action_history:
            return False
        entry = self.action_history.pop()
        frame_number = entry['frame']
        self.current_frame = frame_number
        self.current_layer = entry.get('current_layer', self.current_layer)
        for index, image in entry['layers'].items():
            if 0 <= index < len(self.layers) and frame_number < len(self.layers[index].frames):
                self.layers[index].set_content(frame_number, image.copy())
        self.in_action = False
        self.clear_preview(update=False)
        self.update_canvas()
        return True

    def _compose_without_overlays(self):
        content = self._new_image()
        content_data = content.load()
        checker = self._new_image()
        checker_data = checker.load()
        for x in range(self.width):
            for y in range(self.height):
                checker_data[x, y] = self.bright_gray if (x // 16 + y // 16) % 2 == 0 else self.light_gray

        for index, layer in enumerate(self.layers):
            if not layer.is_active:
                continue
            image = self.preview_images.get(index, layer.get_content(self.current_frame))
            image_data = image.load()
            for x in range(self.width):
                for y in range(self.height):
                    content_data[x, y] = blend_pixels(image_data[x, y], content_data[x, y])

        for x in range(self.width):
            for y in range(self.height):
                content_data[x, y] = blend_pixels(content_data[x, y], checker_data[x, y])
        return content

    def _apply_border(self, image, points):
        if not points:
            return image
        data = image.load()
        for x, y in points:
            if 0 <= x < self.width and 0 <= y < self.height:
                data[x, y] = invert_pixel(data[x, y])
        return image

    def update_canvas(self):
        self.content = self._compose_without_overlays()
        all_points = list(self.overlay_border_points)
        if self.preview_border_points:
            all_points.extend(self.preview_border_points)
        self.content = self._apply_border(self.content, all_points)

    def get_content(self):
        return QPixmap(QImage(self.content.tobytes('raw', 'RGBA'), self.width, self.height, QImage.Format_RGBA8888))

    def show_preview_image(self, image, border_points=None, layer_index=None):
        layer_index = self.current_layer if layer_index is None else layer_index
        self.preview_images = {layer_index: image}
        self.preview_border_points = list(border_points or [])
        self.update_canvas()

    def show_preview_layers(self, preview_images, border_points=None):
        self.preview_images = {index: image for index, image in preview_images.items()}
        self.preview_border_points = list(border_points or [])
        self.update_canvas()

    def clear_preview(self, update=True):
        self.preview_images = {}
        self.preview_border_points = []
        if update:
            self.update_canvas()

    def set_overlay_border(self, points):
        self.overlay_border_points = list(points)
        self.update_canvas()

    def clear_overlay_border(self):
        self.overlay_border_points = []
        self.update_canvas()

    def fill_pixels(self, pixels, display_brush=False, erase=False):
        if not self.layers[self.current_layer].is_active:
            return
        image = self.get_current_image().copy() if display_brush else self.get_current_image()
        data = image.load()
        for xoy, pixel in pixels:
            x, y = xoy
            if 0 <= x < self.width and 0 <= y < self.height:
                data[x, y] = pixel if erase else blend_pixels(pixel, data[x, y])
        if display_brush:
            self.show_preview_image(image)
        else:
            self.clear_preview(update=False)
            self.update_canvas()

    def replace_pixels(self, pixels):
        image = self.get_current_image().copy()
        data = image.load()
        for (x, y), pixel in pixels:
            if 0 <= x < self.width and 0 <= y < self.height:
                data[x, y] = pixel
        self.set_current_image(image)

    def add_frame(self):
        for layer in self.layers:
            image = layer.get_content(len(layer.frames) - 1).copy()
            layer.frames.append(Frame(image))
        self.update_canvas()

    def delete_frame(self, number=None):
        number = self.current_frame if number is None else number
        for layer in self.layers:
            layer.frames.pop(number)
        self.current_frame = self.current_frame - 1 if self.current_frame > 0 else 0
        self.update_canvas()

    def add_layout(self):
        frames = [Frame(self._new_image()) for _ in range(len(self.layers[0].frames))]
        self.layers.append(Layer(frames))
        self.update_canvas()

    def delete_layout(self, number=None):
        number = self.current_layer if number is None else number
        self.current_layer = self.current_layer - 1 if self.current_layer > 0 else 0
        self.layers.pop(number)
        self.update_canvas()

    def _merge_active_layers(self, frame_number):
        content = self._new_image()
        data = content.load()
        for layer in self.layers:
            if not layer.is_active:
                continue
            pixels = layer.get_content(frame_number).load()
            for x in range(self.width):
                for y in range(self.height):
                    data[x, y] = blend_pixels(pixels[x, y], data[x, y])
        return content

    def get_raw(self):
        return self._merge_active_layers(self.current_frame)
