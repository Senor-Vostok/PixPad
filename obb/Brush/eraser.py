from obb.Brush.brush import Brush


class Eraser(Brush):
    def __init__(self, pattern_path, vector_path):
        super().__init__(pattern_path, vector_path)
        self.bag = set()
        self.geometry = [[0, 0]]

    def brush(self, canvas, xoy, k, brushing, app=None):
        if brushing and self.bag:
            canvas.write = False
            self.bag.clear()
        elif not brushing:
            if not canvas.write:
                canvas.history[canvas.current_layer][canvas.current_frame].append([])
                canvas.write = True
            cx = xoy.x() // k
            cy = xoy.y() // k
            data = [((cx + i[0], cy + i[1]), (0, 0, 0, 0)) for i in self.geometry if
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
            canvas.fill_pixels([((cx + i[0], cy + i[1]), (0, 0, 0, 0)) for i in self.geometry if
                                0 <= (cx + i[0]) < canvas.width and 0 <= (cy + i[1]) < canvas.height], True, True)
