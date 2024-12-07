from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QRect


class PixLabel(QLabel):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.func = app.zoom_canvas
        self.inLabel = False
        self.draw = False
        self.brush_func = app.brushes[0].brush
        self.update_func = app.update_canvas
        self.canvas = app.canvas
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        self.draw = True
        scale_factor = self.app.pixmap_canvas.width() / self.app.canvas.brush_frame.image.size[0]
        self.brush_func(self.canvas, event.pos(), scale_factor, not self.draw)
        self.update_func()

    def mouseMoveEvent(self, event):
        scale_factor = self.app.pixmap_canvas.width() / self.app.canvas.brush_frame.image.size[0]
        self.brush_func(self.canvas, event.pos(), scale_factor, not self.draw)
        self.update_func()

    def mouseReleaseEvent(self, event):
        self.draw = False
        self.update_func()

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        self.func(delta) if self.func else None
        event.accept()

    def enterEvent(self, event):
        self.inLabel = True
        event.accept()

    def leaveEvent(self, event):
        self.inLabel = False
        event.accept()
