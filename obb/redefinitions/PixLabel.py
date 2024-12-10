from PyQt5.QtWidgets import QLabel


class PixLabel(QLabel):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.func = app.zoom_canvas
        self.draw = False
        self.update_func = app.update_canvas
        self.scale_factor = 1
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        self.draw = True
        self.app.brush.brush(self.app.canvas, event.pos(), self.scale_factor, not self.draw)
        self.update_func()
        event.accept()

    def mouseMoveEvent(self, event):
        self.app.brush.brush(self.app.canvas, event.pos(), self.scale_factor, not self.draw)
        self.update_func()
        event.accept()

    def mouseReleaseEvent(self, event):
        self.draw = False
        self.app.brush.brush(self.app.canvas, event.pos(), self.scale_factor, not self.draw)
        self.update_func()
        event.accept()

    def enterEvent(self, a0):
        self.scale_factor = self.app.pixmap_canvas.width() / self.app.canvas.content.size[0]
        a0.accept()

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        self.func(delta)
        self.scale_factor = self.app.pixmap_canvas.width() / self.app.canvas.content.size[0]
        event.accept()
