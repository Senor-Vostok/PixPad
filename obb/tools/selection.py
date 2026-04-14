from PIL import Image
from obb.tools.base import BaseTool
from obb.tools.utils import event_to_canvas, normalize_rect, rectangle_outline, make_icon


class SelectionTool(BaseTool):
    def __init__(self, color=(0, 0, 0, 255), size=1):
        super().__init__('Выделение', color, size)
        self.ico = make_icon('selection')
        self.selection_box = None
        self.selection_image = None
        self.base_image = None
        self.anchor_point = None
        self.mode = None
        self.move_press_point = None
        self.move_origin_box = None
        self.preview_box = None

    def has_selection(self):
        return self.selection_box is not None and self.selection_image is not None

    def clear_selection(self, canvas=None):
        self.selection_box = None
        self.selection_image = None
        self.base_image = None
        self.anchor_point = None
        self.mode = None
        self.move_press_point = None
        self.move_origin_box = None
        self.preview_box = None
        if canvas is not None:
            canvas.clear_preview(update=False)
            canvas.overlay_border_points = []
            canvas.update_canvas()

    def _box_contains(self, point):
        if not self.selection_box:
            return False
        left, top, right, bottom = self.selection_box
        x, y = point
        return left <= x <= right and top <= y <= bottom

    def _update_overlay(self, canvas, box):
        left, top, right, bottom = box
        canvas.set_overlay_border(rectangle_outline(left, top, right, bottom))

    def _make_preview_image(self, canvas, box):
        left, top, right, bottom = box
        preview = self.base_image.copy()
        preview_data = preview.load()
        old_left, old_top, old_right, old_bottom = self.selection_box
        for x in range(old_left, old_right + 1):
            for y in range(old_top, old_bottom + 1):
                preview_data[x, y] = (0, 0, 0, 0)
        preview.paste(self.selection_image, (left, top), self.selection_image)
        return preview

    def _clamp_box(self, canvas, box):
        left, top, right, bottom = box
        width = right - left
        height = bottom - top
        left = max(0, min(canvas.width - width - 1, left))
        top = max(0, min(canvas.height - height - 1, top))
        right = left + width
        bottom = top + height
        return left, top, right, bottom

    def on_press(self, canvas, pos, scale, app):
        point = event_to_canvas(pos, scale, canvas)
        if self.has_selection() and self._box_contains(point):
            self.mode = 'move'
            self.move_press_point = point
            self.move_origin_box = self.selection_box
            self.base_image = canvas.get_current_image().copy()
            return
        self.clear_selection(canvas)
        self.mode = 'select'
        self.anchor_point = point
        box = normalize_rect(point, point)
        self.preview_box = box
        canvas.show_preview_image(canvas.get_current_image().copy(), rectangle_outline(*box))

    def on_move(self, canvas, pos, scale, dragging, app):
        point = event_to_canvas(pos, scale, canvas)
        if self.mode == 'select' and self.anchor_point is not None:
            box = normalize_rect(self.anchor_point, point)
            self.preview_box = box
            canvas.show_preview_image(canvas.get_current_image().copy(), rectangle_outline(*box))
        elif self.mode == 'move' and self.move_press_point is not None and self.move_origin_box is not None:
            dx = point[0] - self.move_press_point[0]
            dy = point[1] - self.move_press_point[1]
            left, top, right, bottom = self.move_origin_box
            new_box = self._clamp_box(canvas, (left + dx, top + dy, right + dx, bottom + dy))
            self.preview_box = new_box
            preview = self._make_preview_image(canvas, new_box)
            canvas.show_preview_image(preview, rectangle_outline(*new_box))
        elif not dragging:
            if self.has_selection():
                self._update_overlay(canvas, self.selection_box)
            else:
                canvas.clear_preview()

    def on_release(self, canvas, pos, scale, app):
        if self.mode == 'select' and self.preview_box is not None:
            left, top, right, bottom = self.preview_box
            width = right - left + 1
            height = bottom - top + 1
            current = canvas.get_current_image().copy()
            self.selection_image = current.crop((left, top, right + 1, bottom + 1))
            self.selection_box = (left, top, right, bottom)
            self.base_image = current
            self._update_overlay(canvas, self.selection_box)
            canvas.clear_preview()
        elif self.mode == 'move' and self.preview_box is not None and self.selection_image is not None:
            final_box = self.preview_box
            preview = self._make_preview_image(canvas, final_box)
            canvas.begin_action()
            canvas.set_current_image(preview)
            canvas.end_action()
            self.selection_box = final_box
            self.base_image = preview.copy()
            self._update_overlay(canvas, final_box)
        self.mode = None
        self.anchor_point = None
        self.move_press_point = None
        self.move_origin_box = None
        self.preview_box = None

    def on_leave(self, canvas, app):
        if self.has_selection():
            self._update_overlay(canvas, self.selection_box)
        else:
            canvas.clear_preview()
