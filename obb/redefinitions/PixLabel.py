from PyQt5.QtWidgets import QLabel


class PixLabel(QLabel):
    def __init__(self, func=None):
        super().__init__()
        self.func = func
        self.inLabel = False

    def mousePressEvent(self, event):
        print(f"QFrame: !Mouse pressed at {event.pos()}")

    def mouseMoveEvent(self, event):
        print(f"QFrame: !Mouse moved at {event.pos()}")

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
