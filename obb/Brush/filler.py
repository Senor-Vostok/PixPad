from obb.Brush.simple_brush import SimpleBrush


class Filler(SimpleBrush):

    def __init__(self, pattern_path, vector_path):
        super().__init__(pattern_path, vector_path)
        self.bag = []
        self.painted_color = None
        self.data = None
        self.size = None

    def iterative_fill(self, x, y):
        stack = [(x, y)]
        visited = set()
        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))
            if not (0 <= cx < self.size[0] and 0 <= cy < self.size[1]):
                continue
            if self.data[cx, cy] != self.painted_color:
                continue
            self.bag.append([(cx, cy), self.color])
            stack.extend([(cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)])

    def brush(self, canvas, xoy, k, brushing):
        cx = int(xoy.x() // k)
        cy = int(xoy.y() // k)
        if brushing:
            canvas.fill_pixels([[(cx, cy), self.color]], brushing)
            return
        self.bag.clear()
        self.data = canvas.drawing_data
        self.size = (canvas.width, canvas.height)
        self.painted_color = self.data[cx, cy]
        self.iterative_fill(cx, cy)
        canvas.fill_pixels(self.bag, brushing)
