from PyQt5.QtWidgets import QLabel


class PalLabel(QLabel):
    def __init__(self, app, type_of_palette):
        super().__init__()
        self.app = app
        self.type_of_palette = type_of_palette

    def manager(self, event):
        if self.type_of_palette == "palette":
            self.app.label_colors.setPixmap(self.app.palette.show_palette(xoy=(event.pos().x(), event.pos().y())))
            self.app.label_visibility.setPixmap(self.app.palette.visibility_line())
        elif self.type_of_palette == "colors":
            self.app.label_palette.setPixmap(self.app.palette.colors_line(xoy=(event.pos().x(), event.pos().y())))
            self.app.label_colors.setPixmap(self.app.palette.show_palette(changed_contrast=True))
            self.app.label_visibility.setPixmap(self.app.palette.visibility_line())
        elif self.type_of_palette == "visibility":
            self.app.label_visibility.setPixmap(self.app.palette.visibility_line(xoy=(event.pos().x(), event.pos().y())))
        self.app.brushes[0].color = self.app.palette.color  # brush
        self.app.label_preview.setPixmap(self.app.palette.preview())

    def mousePressEvent(self, event):
        self.manager(event)
        event.accept()

    def mouseMoveEvent(self, event):
        self.manager(event)
        event.accept()