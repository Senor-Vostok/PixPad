from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import sys


class PixPad(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PixPad')
        self.size_of_buttons = 30
        self.init_ui()
        self.showMaximized()

    def init_ui(self):
        left_scroll_area = QScrollArea()
        left_scroll_area.setFrameShape(QFrame.StyledPanel)
        left_scroll_area.setWidgetResizable(True)
        left_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        left_content = QWidget()
        left_layout = QVBoxLayout(left_content)
        left_layout.setAlignment(Qt.AlignTop)
        left_layout.addLayout(self.show_lf())
        left_content.setLayout(left_layout)
        left_scroll_area.setWidget(left_content)

        center_frame = QFrame()
        center_frame.setFrameShape(QFrame.StyledPanel)
        center_frame.setStyleSheet("background-color: white;")  # Временно
        center_frame_layout = QVBoxLayout(center_frame)
        drawing_label = QLabel("Картинка")  # Тут могла быть ваша картинка
        drawing_label.setStyleSheet("background-color: lightgray; border: 2px solid black;")  # Временно
        center_frame_layout.addWidget(drawing_label, alignment=Qt.AlignCenter)

        right_panel = QFrame()
        right_panel.setFrameShape(QFrame.StyledPanel)
        right_layout = QVBoxLayout(right_panel)
        right_layout.addWidget(QPushButton("Кисть"), 3)
        # должны быть кнопки в панели цветов
        colors_layout = QVBoxLayout(right_panel)
        colors_layout.setAlignment(Qt.AlignTop)
        colors_layout.addLayout(self.show_colors([(0, 255, 0), (233, 3, 255), (0, 4, 54), (0, 0, 0), (233, 3, 45), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]))
        right_layout.addLayout(colors_layout, 6)
        right_layout.addWidget(QPushButton("Палитра"), 3)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_scroll_area)
        splitter.addWidget(center_frame)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 70)
        splitter.setStretchFactor(2, 2)

        top_panel = QLabel("Всякие настройки")
        top_panel.setStyleSheet("background-color: pink; padding: 10px; font-size: 16px;")  # Временно
        top_panel.setAlignment(Qt.AlignCenter)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(top_panel, 1)
        main_layout.addWidget(splitter, 15)

    def show_lf(self, count_layouts=1, count_frames=1):
        # Надо каждую из кнопок привязать к своему слою
        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(1)
        grid_layout.setVerticalSpacing(1)
        for i in range(count_layouts):
            layout_button = QPushButton(f"C{i + 1}")
            layout_button.setFixedSize(self.size_of_buttons, self.size_of_buttons)
            grid_layout.addWidget(layout_button, 0, i)
            for j in range(count_frames):
                frame_button = QPushButton(f"F{j + 1}")
                frame_button.setFixedSize(self.size_of_buttons, self.size_of_buttons)
                grid_layout.addWidget(frame_button, j + 1, i)
        #  Тут надо логику для добавления добавить
                if i == count_layouts - 1 and j == count_frames - 1:
                    layout_button = QPushButton(f"+")
                    layout_button.setFixedSize(self.size_of_buttons, self.size_of_buttons)
                    grid_layout.addWidget(layout_button, j + 2, 0)
            if i == count_layouts - 1:
                layout_button = QPushButton(f"+")
                layout_button.setFixedSize(self.size_of_buttons, self.size_of_buttons)
                grid_layout.addWidget(layout_button, 0, i + 1)
        # Тут надо логику для добавления добавить
        return grid_layout

    def show_colors(self, colors):
        color_grid_layout = QGridLayout()
        color_grid_layout.setHorizontalSpacing(1)
        color_grid_layout.setVerticalSpacing(1)
        max_columns = 7
        for i, color in enumerate(colors):
            color_button = QPushButton()
            color_button.setFixedSize(self.size_of_buttons, self.size_of_buttons)
            color_button.setStyleSheet(f"background-color: rgb({color[0]}, {color[1]}, {color[2]});")
            row = i // max_columns
            col = i % max_columns
            color_grid_layout.addWidget(color_button, row, col)
        return color_grid_layout


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PixPad()
    window.show()
    sys.exit(app.exec_())
