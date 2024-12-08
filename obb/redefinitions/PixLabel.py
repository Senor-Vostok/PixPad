from PyQt5.QtWidgets import QLabel


class PixLabel(QLabel):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.func = app.zoom_canvas
        self.draw = False
        self.brush_func = app.brushes[0].brush
        self.update_func = app.update_canvas
        self.canvas = app.canvas
        self.scale_factor = 1
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        self.draw = True
        self.brush_func(self.canvas, event.pos(), self.scale_factor, not self.draw)
        self.update_func()
        event.accept()

    def mouseMoveEvent(self, event):
        self.brush_func(self.canvas, event.pos(), self.scale_factor, not self.draw)
        self.update_func()
        event.accept()

    def mouseReleaseEvent(self, event):
        self.draw = False
        event.accept()

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        self.func(delta)
        self.scale_factor = self.app.pixmap_canvas.width() / self.app.canvas.content.size[0]
        event.accept()
