from math import sqrt
from obb.Brush.simple_brush import SimpleBrush


class Brush(SimpleBrush):
    def __init__(self, pattern_path, vector_path):
        super().__init__(pattern_path, vector_path)
        self.init_brush()
        self.bag = set()

    def init_brush(self):
        self.get_parametrs()
        self.resize(1)

    def get_parametrs(self):
        with open(self.pattern_path, mode='rt') as f:
            for i in f.readlines():
                if 'cx' in i and 'inkscape' not in i:
                    i = i.replace('cx="', '').replace('"', '').split()
                    self.cx = float(i[0])
                if 'cy' in i and 'inkscape' not in i:
                    i = i.replace('cy="', '').replace('"', '').split()
                    self.cy = float(i[0])
                if 'rx' in i and 'inkscape' not in i:
                    i = i.replace('rx="', '').replace('"', '').split()
                    self.base_rx = float(i[0])
                if 'ry' in i and 'inkscape' not in i:
                    i = i.replace('ry="', '').replace('"', '').split()
                    self.base_ry = float(i[0])

    def resize(self, new_size=1):
        scale = new_size / self.base_size
        self.size = new_size
        rx = float(self.base_rx * scale)
        ry = float(self.base_ry * scale)
        if self.size <= 3:
            self.geometry = [[0, 0], [1, 0], [0, 1], [1, 1]] if self.size == 2 else [[0, 0]]
            self.geometry = [[0, 0], [1, 0], [0, 1], [-1, 0], [0, -1]] if self.size == 3 else self.geometry
            return
        cells = []
        for x in range(round(-rx), round(rx + 1)):
            for y in range(round(-ry), round(ry + 1)):
                if sqrt((x ** 2) / max(1, round(rx)) ** 2 + (y ** 2) / max(1, round(ry)) ** 2) <= 1:
                    cells.append((x, y))
        self.geometry = cells

    def _build_pixels(self, canvas, point):
        cx, cy = point
        data = []
        for dx, dy in self.geometry:
            x = cx + dx
            y = cy + dy
            if 0 <= x < canvas.width and 0 <= y < canvas.height:
                data.append(((x, y), self.color))
        return data

    def _draw_unique(self, canvas, point):
        extra_data = []
        for pixel in self._build_pixels(canvas, point):
            if pixel not in self.bag:
                extra_data.append(pixel)
                self.bag.add(pixel)
        if extra_data:
            canvas.fill_pixels(extra_data)

    def on_press(self, canvas, pos, scale, app):
        canvas.begin_action()
        self.bag.clear()
        point = (int(pos.x() // scale), int(pos.y() // scale))
        self._draw_unique(canvas, point)

    def on_move(self, canvas, pos, scale, dragging, app):
        point = (int(pos.x() // scale), int(pos.y() // scale))
        if dragging:
            self._draw_unique(canvas, point)
        else:
            canvas.fill_pixels(self._build_pixels(canvas, point), display_brush=True)

    def on_release(self, canvas, pos, scale, app):
        point = (int(pos.x() // scale), int(pos.y() // scale))
        self._draw_unique(canvas, point)
        self.bag.clear()
        canvas.end_action()
