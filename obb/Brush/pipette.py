from obb.Brush.simple_brush import SimpleBrush


class Pipette(SimpleBrush):
    def __init__(self, pattern_path, vector_path):
        super().__init__(pattern_path, vector_path)

    def brush(self, canvas, xoy, k, brushing, app=None):
        cx = xoy.x() // k
        cy = xoy.y() // k
        if not brushing:
            self.color = canvas.content_data[cx, cy]
            app.change_color(self.color)
