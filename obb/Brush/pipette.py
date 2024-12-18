from obb.Brush.simple_brush import SimpleBrush
from obb.colorhelper import blend_pixels


class Pipette(SimpleBrush):
    def __init__(self, pattern_path, vector_path):
        super().__init__(pattern_path, vector_path)

    def brush(self, canvas, xoy, k, brushing, app=None):
        cx = xoy.x() // k
        cy = xoy.y() // k
        if not brushing:
            pix_bottom = (0, 0, 0, 0)
            for layer in canvas.layers[:canvas.current_layer]:
                matrix = layer.get_content(canvas.current_frame).load()  # Надо иконы поставить, чтобы не лагало
                pix_bottom = blend_pixels(matrix[cx, cy], pix_bottom)
            self.color = blend_pixels(blend_pixels(canvas.after_data[cx, cy], canvas.drawing_data[cx, cy]), pix_bottom)
            app.change_color(self.color)
