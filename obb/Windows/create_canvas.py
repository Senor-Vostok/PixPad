from PyQt5.QtWidgets import QMessageBox, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from obb.styles import WARNING_SCALE, SCALE_WARNING


def on_create_button_click(width_input, height_input, window) -> None:
    width = int(width_input.text())
    height = int(height_input.text())
    if width * height >= SCALE_WARNING:
        QMessageBox.warning(window, "Большое разрешение", WARNING_SCALE)
    elif width <= 0 or height <= 0:
        raise ValueError("Размеры должны быть положительными числами.")
    window.function((width, height))
    window.close()


class ImageSizeWindow(QWidget):
    def __init__(self, function):
        super().__init__()
        self.init_ui()
        self.function = function

    def init_ui(self):
        self.setWindowTitle("Создать изображение")
        layout = QVBoxLayout()
        self.width_label = QLabel("Ширина (px):")
        layout.addWidget(self.width_label)
        self.width_input = QLineEdit()
        layout.addWidget(self.width_input)
        self.height_label = QLabel("Высота (px):")
        layout.addWidget(self.height_label)
        self.height_input = QLineEdit()
        layout.addWidget(self.height_input)
        self.create_button = QPushButton("Создать")
        self.create_button.clicked.connect(lambda: on_create_button_click(self.width_input, self.height_input, self))
        layout.addWidget(self.create_button)
        self.setLayout(layout)