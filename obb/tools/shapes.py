from obb.tools.base import BaseTool
from obb.tools.utils import (
    event_to_canvas,
    bresenham_line,
    ellipse_border_points,
    square_border_points,
    triangle_border_points,
    expand_points,
    clip_points,
    make_icon,
)


class ShapeTool(BaseTool):
    def __init__(self, name, kind, color=(0, 0, 0, 255), size=1):
        super().__init__(name, color, size)
        self.kind = kind
        self.ico = make_icon(kind)
        self.start_point = None
        self.preview_points = []
        self.dragging = False

    def _build_shape_points(self, start, end):
        if self.kind == 'line':
            points = bresenham_line(*start, *end)
        elif self.kind == 'ellipse':
            points = ellipse_border_points(start, end)
        elif self.kind == 'square':
            points = square_border_points(start, end)
        else:
            points = triangle_border_points(start, end)
        points = expand_points(points, self.size)
        return points

    def _preview(self, canvas, end):
        if self.start_point is None:
            return
        points = clip_points(self._build_shape_points(self.start_point, end), canvas)
        self.preview_points = points
        canvas.fill_pixels([((x, y), self.color) for x, y in points], display_brush=True)

    def on_press(self, canvas, pos, scale, app):
        self.start_point = event_to_canvas(pos, scale, canvas)
        self.dragging = True
        self.preview_points = []

    def on_move(self, canvas, pos, scale, dragging, app):
        if not self.dragging or self.start_point is None:
            canvas.clear_preview()
            return
        self._preview(canvas, event_to_canvas(pos, scale, canvas))

    def on_release(self, canvas, pos, scale, app):
        if self.start_point is None:
            return
        end_point = event_to_canvas(pos, scale, canvas)
        points = clip_points(self._build_shape_points(self.start_point, end_point), canvas)
        canvas.begin_action()
        canvas.fill_pixels([((x, y), self.color) for x, y in points])
        canvas.end_action()
        self.start_point = None
        self.preview_points = []
        self.dragging = False

    def on_leave(self, canvas, app):
        if not self.dragging:
            canvas.clear_preview()
