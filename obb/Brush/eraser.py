from obb.Brush.brush import Brush


class Eraser(Brush):
    def __init__(self, pattern_path, vector_path):
        super().__init__(pattern_path, vector_path)
        self.bag = set()
        self.geometry = [[0, 0]]

    def brush(self, canvas, xoy, k, brushing):
        if brushing and self.bag:
            canvas.fill_pixels(self.bag, False, True)
            self.bag.clear()
        elif not brushing:
            cx = xoy.x() // k
            cy = xoy.y() // k
            data = [((cx + i[0], cy + i[1]), self.color) for i in self.geometry if
                    0 <= (cx + i[0]) < canvas.width and 0 <= (cy + i[1]) < canvas.height]
            extra_data = list()
            for pixel in data:
                if pixel not in self.bag:
                    extra_data.append(pixel)
                    self.bag.add(pixel)
            canvas.fill_pixels(extra_data, False, True)
        else:
            cx = xoy.x() // k
            cy = xoy.y() // k
            canvas.fill_pixels([((cx + i[0], cy + i[1]), self.color) for i in self.geometry if
                                0 <= (cx + i[0]) < canvas.width and 0 <= (cy + i[1]) < canvas.height], True, True)
