from collections import deque
import numpy as np
from obb.Brush.simple_brush import SimpleBrush


class Filler(SimpleBrush):
    def __init__(self, pattern_path, vector_path):
        super().__init__(pattern_path, vector_path)
        self.bag = []
        self.painted_color = None
        self.data = None
        self.size_depth = None

    def iterative_fill(self, x, y):
        queue = deque([(x, y)])
        visited = np.zeros(self.size_depth, dtype=bool)
        visited[x, y] = True
        while queue:
            cx, cy = queue.popleft()
            if not (0 <= cx < self.size_depth[0] and 0 <= cy < self.size_depth[1]):
                continue
            if not np.array_equal(self.data[cx, cy], self.painted_color):
                continue
            self.bag.append(((cx, cy), self.color))
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.size_depth[0] and 0 <= ny < self.size_depth[1] and not visited[nx, ny]:
                    visited[nx, ny] = True
                    queue.append((nx, ny))

    def on_press(self, canvas, pos, scale, app):
        cx = int(pos.x() // scale)
        cy = int(pos.y() // scale)
        if not (0 <= cx < canvas.width and 0 <= cy < canvas.height):
            return
        canvas.begin_action()
        self.bag.clear()
        self.data = canvas.get_current_image().load()
        self.size_depth = (canvas.width, canvas.height)
        self.painted_color = self.data[cx, cy]
        if self.painted_color == self.color:
            canvas.end_action()
            return
        self.iterative_fill(cx, cy)
        canvas.fill_pixels(self.bag)
        canvas.end_action()

    def on_move(self, canvas, pos, scale, dragging, app):
        canvas.clear_preview()

    def on_release(self, canvas, pos, scale, app):
        pass
