from obb.tools.base import BaseTool
from obb.tools.utils import event_to_canvas, shift_image, make_icon


class LayerMoveTool(BaseTool):
    def __init__(self, color=(0, 0, 0, 255), size=1):
        super().__init__('Перемещение слоёв', color, size)
        self.ico = make_icon('move_layers')
        self.start_point = None
        self.original_images = {}
        self.layer_indices = []
        self.last_delta = (0, 0)
        self.dragging = False

    def _get_target_layers(self, canvas, app):
        selected = sorted(index for index in app.selected_layers if 0 <= index < len(canvas.layers))
        return selected or [canvas.current_layer]

    def _build_preview(self, canvas, dx, dy):
        preview = {}
        for index, image in self.original_images.items():
            preview[index] = shift_image(image, dx, dy, (canvas.width, canvas.height), canvas.background_color)
        return preview

    def on_press(self, canvas, pos, scale, app):
        self.start_point = event_to_canvas(pos, scale, canvas)
        self.layer_indices = self._get_target_layers(canvas, app)
        self.original_images = {index: canvas.get_layer_image(index).copy() for index in self.layer_indices}
        self.last_delta = (0, 0)
        self.dragging = True

    def on_move(self, canvas, pos, scale, dragging, app):
        if not self.dragging or self.start_point is None:
            canvas.clear_preview()
            return
        current = event_to_canvas(pos, scale, canvas)
        dx = current[0] - self.start_point[0]
        dy = current[1] - self.start_point[1]
        self.last_delta = (dx, dy)
        canvas.show_preview_layers(self._build_preview(canvas, dx, dy))

    def on_release(self, canvas, pos, scale, app):
        if self.start_point is None:
            return
        dx, dy = self.last_delta
        if dx == 0 and dy == 0:
            canvas.clear_preview()
        else:
            canvas.begin_action(self.layer_indices)
            for index, image in self.original_images.items():
                moved = shift_image(image, dx, dy, (canvas.width, canvas.height), canvas.background_color)
                canvas.set_layer_image(index, moved, update=False)
            canvas.end_action()
        self.start_point = None
        self.original_images = {}
        self.layer_indices = []
        self.last_delta = (0, 0)
        self.dragging = False

    def on_leave(self, canvas, app):
        if not self.dragging:
            canvas.clear_preview()
