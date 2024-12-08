from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from obb.styles import *
from obb.initialization import *
from PyQt5.Qt import QIcon, QColor
import sys
from obb.redefinitions.PixFrame import PixFrame
from obb.redefinitions.PixLabel import PixLabel
from obb.redefinitions.PalLabel import PalLabel


class PixPad(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PixPad')

        self.shadow_effect = QGraphicsDropShadowEffect(self)

        self.grid_layout = QGridLayout()

        self.brushes = init_brushes()

        self.canvas = init_canvas((960, 540))

        self.palette = init_palette()
        self.label_preview = QLabel()
        self.label_preview.setPixmap(self.palette.preview())
        self.label_visibility = PalLabel(self, "visibility")
        self.label_visibility.setPixmap(self.palette.visibility_line())
        self.label_palette = PalLabel(self, "colors")
        self.label_palette.setPixmap(self.palette.colors_line())
        self.label_colors = PalLabel(self, "palette")
        self.label_colors.setPixmap(self.palette.show_palette())

        self.brushes[0].color = self.palette.color

        self.speed_zoom = 2

        self.drawing_label = PixLabel(self)
        self.pixmap_canvas = self.canvas.get_content()

        self.size_of_buttons = 30

        self.init_ui()
        self.showMaximized()

    def init_ui(self):
        self.shadow_effect.setBlurRadius(20)
        self.shadow_effect.setXOffset(5)
        self.shadow_effect.setYOffset(5)
        self.shadow_effect.setColor(QColor(0, 0, 0, 160))

        self.setStyleSheet("background-color: rgb(51, 51, 51)")
        left_scroll_area = QScrollArea(self)
        left_scroll_area.setFrameShape(QFrame.StyledPanel)
        left_scroll_area.setWidgetResizable(True)
        left_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        left_content = QWidget()
        left_content.setStyleSheet("background-color: rgb(32, 33, 37);border-radius: 5px;border: 4px solid rgba(0, 0, 0, 255);")
        left_layout = QVBoxLayout(left_content)
        left_layout.setAlignment(Qt.AlignTop)
        self.show_lf(len(self.canvas.layers), len(self.canvas.layers[0].frames))
        left_layout.addLayout(self.grid_layout)
        left_content.setLayout(left_layout)
        left_scroll_area.setWidget(left_content)

        center_frame = PixFrame(self.zoom_canvas)
        center_frame.setFrameShape(QFrame.StyledPanel)
        center_frame.setWidgetResizable(True)
        center_frame.setStyleSheet("background-color: rgb(32, 33, 37);border-radius: 5px;border: 4px solid rgba(0, 0, 0, 255);")
        self.update_canvas()
        center_frame.setAlignment(Qt.AlignCenter)
        center_frame.setWidget(self.drawing_label)

        right_panel = QFrame(self)
        right_panel.setStyleSheet("background-color: rgb(32, 33, 37);border-radius: 5px;border: 4px solid rgba(0, 0, 0, 255);")
        right_panel.setFrameShape(QFrame.StyledPanel)
        right_layout = QVBoxLayout(right_panel)
        right_layout.addLayout(self.show_brushes(self.brushes))
        colors_layout = QVBoxLayout(right_panel)
        colors_layout.setAlignment(Qt.AlignTop)
        colors_layout.addLayout(self.show_colors(
            [(0, 255, 0), (233, 3, 255), (0, 4, 54), (0, 0, 0), (233, 3, 45), (255, 0, 0), (0, 255, 0), (0, 0, 255),
             (255, 255, 0)]))  # Временно
        right_layout.addLayout(colors_layout, 6)
        right_layout.addLayout(self.show_palette())

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_scroll_area)
        splitter.addWidget(center_frame)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 18)

        top_panel = QHBoxLayout()
        file = QPushButton("Файл")
        top_panel.addWidget(file)
        top_panel.setAlignment(Qt.AlignLeft)

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(top_panel, 1)
        work_layout = QHBoxLayout(self)
        work_layout.addWidget(splitter, 10)
        work_layout.addWidget(right_panel, 1)
        main_layout.addLayout(work_layout, 30)

    def show_lf(self, count_layouts=1, count_frames=1):
        self.grid_layout.setHorizontalSpacing(10)
        self.grid_layout.setVerticalSpacing(5)
        for i in range(count_layouts):
            layout_button = QPushButton()
            layout_button.setStyleSheet(BUTTON_LAYOUT)
            layout_button.setFixedSize(self.size_of_buttons, self.size_of_buttons)
            layout_button.clicked.connect(lambda _, x=i: self.hide_show_layer(x))
            self.grid_layout.addWidget(layout_button, 0, i)
            for j in range(count_frames):
                frame_button = QPushButton()
                frame_button.setStyleSheet(BUTTON_FRAME)
                frame_button.setFixedSize(self.size_of_buttons, self.size_of_buttons)
                frame_button.clicked.connect(lambda _, x=i, y=j: self.change_frame(y + 1, x))
                self.grid_layout.addWidget(frame_button, j + 1, i)
                if i == count_layouts - 1 and j == count_frames - 1:
                    layout_button = QPushButton()
                    layout_button.setStyleSheet(BUTTON_PLUS)
                    layout_button.setFixedSize(self.size_of_buttons, self.size_of_buttons)
                    layout_button.clicked.connect(self.add_frame)
                    self.grid_layout.addWidget(layout_button, j + 2, 0)
            if i == count_layouts - 1:
                layout_button = QPushButton()
                layout_button.setStyleSheet(BUTTON_PLUS)
                layout_button.setFixedSize(self.size_of_buttons, self.size_of_buttons)
                layout_button.clicked.connect(self.add_layout)
                self.grid_layout.addWidget(layout_button, 0, i + 1)

    def hide_show_layer(self, number_layer):
        self.canvas.layers[number_layer].is_active = not self.canvas.layers[number_layer].is_active
        layout_button = QPushButton()
        layout_button.setStyleSheet(BUTTON_LAYOUT if self.canvas.layers[number_layer].is_active else BUTTON_LAYOUT_D)
        layout_button.setFixedSize(self.size_of_buttons, self.size_of_buttons)
        layout_button.clicked.connect(lambda _, x=number_layer: self.hide_show_layer(x))
        self.grid_layout.addWidget(layout_button, 0, number_layer)
        self.canvas.update_canvas()
        self.update_canvas()

    def change_frame(self, number_frame, number_layer):
        self.canvas.current_layer = number_layer
        self.canvas.current_frame = number_frame - 1
        self.canvas.update_canvas()
        self.update_canvas()

    def add_frame(self):
        count = len(self.canvas.layers[0].frames)
        for i in range(len(self.canvas.layers)):
            frame_button = QPushButton()
            frame_button.setStyleSheet(BUTTON_FRAME)
            frame_button.setFixedSize(self.size_of_buttons, self.size_of_buttons)
            frame_button.clicked.connect(lambda _, x=i: self.change_frame(count + 1, x))
            self.grid_layout.addWidget(frame_button, count + 1, i)
        layout_button = QPushButton()
        layout_button.setStyleSheet(BUTTON_PLUS)
        layout_button.setFixedSize(self.size_of_buttons, self.size_of_buttons)
        layout_button.clicked.connect(self.add_frame)
        self.grid_layout.addWidget(layout_button, count + 2, 0)
        self.canvas.add_frame()

    def add_layout(self):
        count = len(self.canvas.layers)
        layout_button = QPushButton()
        layout_button.setStyleSheet(BUTTON_LAYOUT)
        layout_button.setFixedSize(self.size_of_buttons, self.size_of_buttons)
        layout_button.clicked.connect(lambda _, x=count: self.hide_show_layer(x))
        self.grid_layout.addWidget(layout_button, 0, count)
        for i in range(len(self.canvas.layers[0].frames)):
            frame_button = QPushButton()
            frame_button.setStyleSheet(BUTTON_FRAME)
            frame_button.setFixedSize(self.size_of_buttons, self.size_of_buttons)
            frame_button.clicked.connect(lambda _, x=i, b=count: self.change_frame(x + 1, b))
            self.grid_layout.addWidget(frame_button, i + 1, count)
        layout_button = QPushButton()
        layout_button.setStyleSheet(BUTTON_PLUS)
        layout_button.setFixedSize(self.size_of_buttons, self.size_of_buttons)
        layout_button.clicked.connect(self.add_layout)
        self.grid_layout.addWidget(layout_button, 0, count + 1)
        self.canvas.add_layout()

    def update_canvas(self, width=None, height=None):
        if not width or not height:
            width, height = self.pixmap_canvas.width(), self.pixmap_canvas.height()
        self.pixmap_canvas = self.canvas.get_content().scaled(width, height, Qt.KeepAspectRatio)
        if width and height:
            self.drawing_label.setFixedSize(self.pixmap_canvas.width(), self.pixmap_canvas.height())
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

    def show_palette(self):
        layout = QVBoxLayout()
        layout.addWidget(self.label_preview)
        layout.addWidget(self.label_visibility)
        layout.addWidget(self.label_palette)
        layout.addWidget(self.label_colors)
        return layout


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PixPad()
    window.show()
    sys.exit(app.exec_())
