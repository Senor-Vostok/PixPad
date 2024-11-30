from PyQt5.QtWidgets import QFrame


class PixFrame(QFrame):
    def __init__(self, func=None):
        super().__init__()
        self.func = func

    def mousePressEvent(self, event):
        print(f"QFrame: Mouse pressed at {event.pos()}")

    def mouseMoveEvent(self, event):
        print(f"QFrame: Mouse moved at {event.pos()}")

    def mouseReleaseEvent(self, event):
        print(f"QFrame: Mouse released at {event.pos()}")

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        if delta > 0:
            print("Scrolled up")
        else:
            print("Scrolled down")
        event.accept()
