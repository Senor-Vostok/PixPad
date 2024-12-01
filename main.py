from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from obb.styles import *
from obb.initialization import *
from PyQt5.Qt import QIcon
import sys
from obb.redefinitions.PixFrame import PixFrame
from obb.redefinitions.PixLabel import PixLabel


class PixPad(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PixPad')
        self.brushes = init_brushes()
        self.canvas = init_canvas((20, 40))
        self.speed_zoom = 2
        self.drawing_label = PixLabel(self)
        self.pixmap_canvas = self.canvas.get_content()
        self.size_of_buttons = 30
        self.init_ui()
        self.showMaximized()

    def init_ui(self):
        self.setStyleSheet("background-color: rgb(88, 108, 108);")
        left_scroll_area = QScrollArea(self)
        left_scroll_area.setFrameShape(QFrame.StyledPanel)
        left_scroll_area.setWidgetResizable(True)
        left_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        left_content = QWidget()
        left_content.setStyleSheet("background-color: rgb(99, 105, 105);")
        left_layout = QVBoxLayout(left_content)
        left_layout.setAlignment(Qt.AlignTop)
        left_layout.addLayout(self.show_lf(len(self.canvas.layers), len(self.canvas.layers[0].frames)))
        left_content.setLayout(left_layout)
        left_scroll_area.setWidget(left_content)

        center_frame = PixFrame(self.zoom_canvas)
        center_frame.setFrameShape(QFrame.StyledPanel)
        center_frame.setStyleSheet("background-color: rgb(52, 58, 59);")
        center_frame_layout = QVBoxLayout(center_frame)
        self.update_canvas()
        center_frame_layout.addWidget(self.drawing_label, alignment=Qt.AlignCenter)

        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: rgb(99, 105, 105);")
        right_panel.setFrameShape(QFrame.StyledPanel)
        right_layout = QVBoxLayout(right_panel)
        right_layout.addLayout(self.show_brushes(self.brushes * 23))
        colors_layout = QVBoxLayout(right_panel)
        colors_layout.setAlignment(Qt.AlignTop)
        colors_layout.addLayout(self.show_colors(
            [(0, 255, 0), (233, 3, 255), (0, 4, 54), (0, 0, 0), (233, 3, 45), (255, 0, 0), (0, 255, 0), (0, 0, 255),
             (255, 255, 0)]))  # Временно
        right_layout.addLayout(colors_layout, 6)
        right_layout.addWidget(QPushButton("Палитра"), 3)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_scroll_area)
        splitter.addWidget(center_frame)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 18)

        top_panel = QLabel("Всякие настройки")
        top_panel.setStyleSheet("padding: 10px; font-size: 16px;")  # Временно
        top_panel.setAlignment(Qt.AlignCenter)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(top_panel, 1)
        work_layout = QHBoxLayout(self)
        work_layout.addWidget(splitter, 10)
        work_layout.addWidget(right_panel, 1)
        main_layout.addLayout(work_layout, 30)

    def show_lf(self, count_layouts=1, count_frames=1):
        # Надо каждую из кнопок привязать к своему слою
        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(10)
        grid_layout.setVerticalSpacing(5)
        for i in range(count_layouts):
            layout_button = QPushButton()
            layout_button.setStyleSheet(BUTTON_LAYOUT)
            layout_button.setFixedSize(self.size_of_buttons, self.size_of_buttons)
            grid_layout.addWidget(layout_button, 0, i)
            for j in range(count_frames):
                frame_button = QPushButton()
                frame_button.setStyleSheet(BUTTON_FRAME)
                frame_button.setFixedSize(self.size_of_buttons, self.size_of_buttons)
                grid_layout.addWidget(frame_button, j + 1, i)
                if i == count_layouts - 1 and j == count_frames - 1:
                    layout_button = QPushButton()
                    layout_button.setStyleSheet(BUTTON_PLUS)
                    layout_button.setFixedSize(self.size_of_buttons, self.size_of_buttons)
                    grid_layout.addWidget(layout_button, j + 2, 0)
            if i == count_layouts - 1:
                layout_button = QPushButton()
                layout_button.setStyleSheet(BUTTON_PLUS)
                layout_button.setFixedSize(self.size_of_buttons, self.size_of_buttons)
                grid_layout.addWidget(layout_button, 0, i + 1)
        return grid_layout

    def update_canvas(self, width=None, height=None):
        if not width or not height:
            width, height = self.pixmap_canvas.width(), self.pixmap_canvas.height()
        del self.pixmap_canvas
        self.pixmap_canvas = self.canvas.get_content().scaled(width, height, Qt.KeepAspectRatio)
        self.drawing_label.setPixmap(self.pixmap_canvas)

    def zoom_canvas(self, delta):
        if delta > 0:
            width, height = self.pixmap_canvas.width() * self.speed_zoom, self.pixmap_canvas.height() * self.speed_zoom
        else:
            width, height = self.pixmap_canvas.width() // self.speed_zoom, self.pixmap_canvas.height() // self.speed_zoom
        self.update_canvas(width, height)

    def show_colors(self, colors):
        color_grid_layout = QGridLayout()
        color_grid_layout.setHorizontalSpacing(1)
        color_grid_layout.setVerticalSpacing(1)
        max_columns = 7
        for i, color in enumerate(colors):
            color_button = QPushButton()
            color_button.setFixedSize(self.size_of_buttons, self.size_of_buttons)
            if sum(color) / 3 <= 128:
                color_button.setStyleSheet(BUTTON_BRIGHT.split('<<color>>')[0] + ', '.join(str(j) for j in color) +
                                           BUTTON_BRIGHT.split('<<color>>')[1])
            else:
                color_button.setStyleSheet(BUTTON_DARK.split('<<color>>')[0] + ', '.join(str(j) for j in color) +
                                           BUTTON_DARK.split('<<color>>')[1])
            row = i // max_columns
            col = i % max_columns
            color_grid_layout.addWidget(color_button, row, col)
        return color_grid_layout

    def show_brushes(self, brushes, current_brush=None):
        if not current_brush:
            current_brush = brushes[0]
        brushes_layout = QHBoxLayout()
        main_brush = QLabel(self)
        main_brush.setPixmap(current_brush.get_ico([100, 100]))
        brushes_layout.addWidget(main_brush)
        grid_brush = QGridLayout()
        grid_brush.setHorizontalSpacing(0)
        grid_brush.setVerticalSpacing(0)
        max_column = 4
        for i, brush in enumerate(brushes):
            button_brush = QPushButton()
            button_brush.setStyleSheet(BUTTON_BRUSH)
            button_brush.setFixedSize(self.size_of_buttons, self.size_of_buttons)
            button_brush.setIcon(QIcon(brush.get_ico()))
            row = i // max_column
            col = i % max_column
            grid_brush.addWidget(button_brush, row, col)
        grid_brush.setAlignment(Qt.AlignTop)
        brushes_layout.addLayout(grid_brush)
        return brushes_layout

    def show_palette(self, current_palette, palettes, chosen_color):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PixPad()
    window.show()
    sys.exit(app.exec_())
