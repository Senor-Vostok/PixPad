from PyQt5.QtWidgets import QLabel


class PixLabel(QLabel):
    def __init__(self, func=None, brush_func=None, update_func=None, canvas=None):
        super().__init__()
        self.func = func
        self.inLabel = False
        self.brush_func = brush_func
        self.update_func = update_func
        self.canvas = canvas

    def mousePressEvent(self, event):
        print(f"QFrame: !Mouse pressed at {event.pos()}")

    def mouseMoveEvent(self, event):
        print(f"QFrame: !Mouse moved at {event.pos()}")
        self.brush_func(self.canvas, event.pos())
        self.update_func()

    def mouseReleaseEvent(self, event):
        print(f"QFrame: !Mouse released at {event.pos()}")

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
