from PyQt5.QtWidgets import QScrollArea


class PixFrame(QScrollArea):
    def __init__(self, func=None):
        super().__init__()
        self.func = func

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        self.func(delta) if self.func else None
        event.accept()
