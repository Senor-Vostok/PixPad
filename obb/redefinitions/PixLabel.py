from PyQt5.QtWidgets import QLabel


class PixLabel(QLabel):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.func = app.zoom_canvas
        self.update_func = app.update_canvas
        self.scale_factor = 1
        self.dragging = False
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        self.dragging = True
        self.app.current_tool.on_press(self.app.canvas, event.pos(), self.scale_factor, self.app)
        self.update_func()
        event.accept()

    def mouseMoveEvent(self, event):
        self.app.current_tool.on_move(self.app.canvas, event.pos(), self.scale_factor, self.dragging, self.app)
        self.update_func()
        event.accept()

    def mouseReleaseEvent(self, event):
        self.dragging = False
        self.app.current_tool.on_release(self.app.canvas, event.pos(), self.scale_factor, self.app)
        self.update_func()
        event.accept()

    def enterEvent(self, a0):
        self.scale_factor = self.app.pixmap_canvas.width() / self.app.canvas.width if self.app.canvas.width else 1
        a0.accept()

    def leaveEvent(self, event):
        if not self.dragging:
            self.app.current_tool.on_leave(self.app.canvas, self.app)
            self.update_func()
        event.accept()

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        self.func(delta)
        self.scale_factor = self.app.pixmap_canvas.width() / self.app.canvas.width if self.app.canvas.width else 1
        event.accept()
