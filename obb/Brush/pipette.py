from obb.Brush.simple_brush import SimpleBrush


class Pipette(SimpleBrush):
    def __init__(self, pattern_path, vector_path):
        super().__init__(pattern_path, vector_path)

    def on_press(self, canvas, pos, scale, app):
        cx = int(pos.x() // scale)
        cy = int(pos.y() // scale)
        if not (0 <= cx < canvas.width and 0 <= cy < canvas.height):
            return
        self.color = canvas.get_raw().load()[cx, cy]
        app.change_color(self.color)

    def on_move(self, canvas, pos, scale, dragging, app):
        canvas.clear_preview()

    def on_release(self, canvas, pos, scale, app):
        pass
