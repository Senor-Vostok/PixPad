from obb.Brush.brush import Brush


class Eraser(Brush):
    def __init__(self, pattern_path, vector_path):
        super().__init__(pattern_path, vector_path)
        self.geometry = [[0, 0]]

    def _build_pixels(self, canvas, point):
        cx, cy = point
        data = []
        for dx, dy in self.geometry:
            x = cx + dx
            y = cy + dy
            if 0 <= x < canvas.width and 0 <= y < canvas.height:
                data.append(((x, y), (0, 0, 0, 0)))
        return data

    def _draw_unique(self, canvas, point):
        extra_data = []
        for pixel in self._build_pixels(canvas, point):
            if pixel not in self.bag:
                extra_data.append(pixel)
                self.bag.add(pixel)
        if extra_data:
            canvas.fill_pixels(extra_data, erase=True)

    def on_move(self, canvas, pos, scale, dragging, app):
        point = (int(pos.x() // scale), int(pos.y() // scale))
        if dragging:
            self._draw_unique(canvas, point)
        else:
            canvas.fill_pixels(self._build_pixels(canvas, point), display_brush=True, erase=True)
