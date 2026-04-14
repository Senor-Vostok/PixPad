from PyQt5.QtGui import QPixmap


class BaseTool:
    def __init__(self, name, color=(0, 0, 0, 255), size=1):
        self.name = name
        self.color = color
        self.size = size
        self.ico = QPixmap()

    def resize(self, new_size):
        self.size = max(1, int(new_size))

    def get_ico(self, current_size=None):
        if current_size:
            return self.ico.scaled(current_size[0], current_size[1])
        return self.ico

    def on_press(self, canvas, pos, scale, app):
        pass

    def on_move(self, canvas, pos, scale, dragging, app):
        pass

    def on_release(self, canvas, pos, scale, app):
        pass

    def on_leave(self, canvas, app):
        canvas.clear_preview()
