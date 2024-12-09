from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QByteArray
from obb.styles import *
from obb.initialization import *
from PyQt5.Qt import QIcon, QColor
import sys
from obb.redefinitions.PixFrame import PixFrame
from obb.redefinitions.PixLabel import PixLabel
from obb.redefinitions.PalLabel import PalLabel
from obb.savefile import *


class PixPad(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PixPad')

        self.size_of_buttons = 30

        self.shadow_effect = QGraphicsDropShadowEffect(self)

        self.grid_layout = QGridLayout()

        self.brushes = init_brushes()
        self.brush = self.brushes[0]

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
        self.colors = [(0, 0, 0, 255), (34, 32, 52, 255), (69, 40, 60, 255), (102, 57, 49, 255), (143, 86, 59, 255),
                       (223, 113, 38, 255), (217, 160, 102, 255), (238, 195, 154, 255), (251, 242, 54, 255),
                       (153, 229, 80, 255), (106, 190, 48, 255), (55, 148, 110, 255), (75, 105, 47, 255), (82, 75, 36, 255),
                       (95, 205, 228, 255), (203, 219, 252, 255), (255, 255, 255, 255), (155, 173, 183, 255), (132, 126, 135, 255),
                       (105, 106, 106, 255), (89, 86, 82, 255), (118, 66, 138, 255), (172, 50, 50, 255), (217, 87, 99, 255),
                       (215, 123, 186, 255), (143, 151, 74, 255), (138, 111, 48, 255)]
        self.color_grid_layout = QGridLayout()
        self.color_grid_layout.setHorizontalSpacing(3)
        self.color_grid_layout.setVerticalSpacing(3)
        self.show_colors(self.colors)

        self.brush.color = self.palette.color

        self.speed_zoom = 2

        self.drawing_label = PixLabel(self)
        self.pixmap_canvas = self.canvas.get_content()

        self.init_ui()
        self.showMaximized()

    def init_ui(self):
        self.shadow_effect.setBlurRadius(20)
        self.shadow_effect.setXOffset(5)
        self.shadow_effect.setYOffset(5)
        self.shadow_effect.setColor(QColor(0, 0, 0, 160))

        self.setStyleSheet("background-color: rgb(51, 51, 51)")
        self.left_scroll_area = QScrollArea(self)
        self.left_scroll_area.setFrameShape(QFrame.StyledPanel)
        self.left_scroll_area.setWidgetResizable(True)
        self.left_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.left_content = QWidget()
        self.left_content.setStyleSheet("background-color: rgb(32, 33, 37);border-radius: 5px;border: 4px solid rgba(0, 0, 0, 255);")
        self.left_layout = QVBoxLayout(self.left_content)
        self.left_layout.setAlignment(Qt.AlignTop)
        self.show_lf(len(self.canvas.layers), len(self.canvas.layers[0].frames))
        self.left_layout.addLayout(self.grid_layout)
        self.left_content.setLayout(self.left_layout)
        self.left_scroll_area.setWidget(self.left_content)

        self.center_frame = PixFrame(self.zoom_canvas)
        self.center_frame.setFrameShape(QFrame.StyledPanel)
        self.center_frame.setWidgetResizable(True)
        self.center_frame.setStyleSheet("background-color: rgb(32, 33, 37);border-radius: 5px;border: 4px solid rgba(0, 0, 0, 255);")
        self.update_canvas()

        self.center_frame.setAlignment(Qt.AlignCenter)
        self.center_frame.setWidget(self.drawing_label)

        self.right_panel = QFrame(self)
        self.right_panel.setStyleSheet("background-color: rgb(32, 33, 37);border-radius: 5px;border: 4px solid rgba(0, 0, 0, 255);")
        self.right_panel.setFrameShape(QFrame.StyledPanel)
        self.right_layout = QVBoxLayout(self.right_panel)
        self.right_layout.addLayout(self.show_brushes(self.brushes))
        self.colors_layout = QVBoxLayout(self.right_panel)
        self.colors_layout.setAlignment(Qt.AlignTop)
        self.colors_layout.addLayout(self.color_grid_layout)  # Временно
        self.right_layout.addLayout(self.colors_layout, 6)
        self.right_layout.addLayout(self.show_palette())

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.left_scroll_area)
        self.splitter.addWidget(self.center_frame)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 18)

        self.top_panel = QHBoxLayout()
        self.file = QPushButton("Файл")
        self.file_menu = QMenu()
        self.save_png_action = QAction("Сохранить как PNG", self)
        self.save_png_action.triggered.connect(self.save_canvas_as_png)
        self.file_menu.addAction(self.save_png_action)
        self.file.setMenu(self.file_menu)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(64)
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(lambda _: self.resize_brush())
        self.value_brush = QLabel(f"X{self.slider.value()}")
        self.top_panel.addWidget(self.file)
        self.top_panel.addWidget(self.slider)
        self.top_panel.addWidget(self.value_brush)
        self.top_panel.setAlignment(Qt.AlignLeft)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addLayout(self.top_panel, 1)
        self.work_layout = QHBoxLayout(self)
        self.work_layout.addWidget(self.splitter, 10)
        self.work_layout.addWidget(self.right_panel, 1)
        self.main_layout.addLayout(self.work_layout, 30)

    def change_brush(self, number, label):
        color = self.brush.color
        self.brush = self.brushes[number]
        self.brush.color = color
        label.setPixmap(self.brush.get_ico([100, 100]))

    def resize_brush(self):
        self.brush.resize(self.slider.value())
        self.value_brush.setText(f"X{self.slider.value()}")

    def save_canvas_as_png(self):
        options = QFileDialog.Options()
        filepath, _ = QFileDialog.getSaveFileName(self, "Сохранить как PNG", "", "PNG Files (*.png)", options=options)
        if filepath:
            pil_image = self.canvas.get_raw()
            saver = PixelEditorSaver(self.canvas.width, self.canvas.height, self.canvas.background_color, pil_image)
            saver.save_as_png(filepath)

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

    def change_color(self, color):
        self.palette.color = color
        self.brush.color = color
        self.label_palette.setPixmap(self.palette.colors_line())
        self.label_colors.setPixmap(self.palette.show_palette())
        self.label_visibility.setPixmap(self.palette.visibility_line())
        self.label_preview.setPixmap(self.palette.preview())

    def add_color(self):
        max_columns = 8
        color = self.palette.color
        color_button = QPushButton()
        color_button.setFixedSize(self.size_of_buttons, self.size_of_buttons)
        if sum(color) / 3 <= 128:
            color_button.setStyleSheet(BUTTON_BRIGHT.split('<<color>>')[0] + ', '.join(str(j) for j in color) +
                                       BUTTON_BRIGHT.split('<<color>>')[1])
        else:
            color_button.setStyleSheet(BUTTON_DARK.split('<<color>>')[0] + ', '.join(str(j) for j in color) +
                                       BUTTON_DARK.split('<<color>>')[1])
        color_button.clicked.connect(lambda _, c=color: self.change_color(c))
        row = len(self.colors) // max_columns
        col = len(self.colors) % max_columns
        self.color_grid_layout.addWidget(color_button, row, col)
        self.colors.append(color)

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
        max_columns = 8
        for i, color in enumerate(colors):
            color_button = QPushButton()
            color_button.setFixedSize(self.size_of_buttons, self.size_of_buttons)
            if sum(color) / 3 <= 128:
                color_button.setStyleSheet(BUTTON_BRIGHT.split('<<color>>')[0] + ', '.join(str(j) for j in color) +
                                           BUTTON_BRIGHT.split('<<color>>')[1])
            else:
                color_button.setStyleSheet(BUTTON_DARK.split('<<color>>')[0] + ', '.join(str(j) for j in color) +
                                           BUTTON_DARK.split('<<color>>')[1])
            color_button.clicked.connect(lambda _, c=color: self.change_color(c))
            row = i // max_columns
            col = i % max_columns
            self.color_grid_layout.addWidget(color_button, row, col)

    def show_brushes(self, brushes):
        current_brush = self.brush
        brushes_layout = QHBoxLayout()
        brushes_layout.setAlignment(Qt.AlignLeft)
        main_brush = QLabel(self)
        main_brush.setFixedSize(100, 100)
        main_brush.setPixmap(current_brush.get_ico([100, 100]))
        brushes_layout.addWidget(main_brush)
        grid_brush = QGridLayout()
        grid_brush.setHorizontalSpacing(0)
        grid_brush.setVerticalSpacing(0)
        max_column = 4
        for i, brush in enumerate(brushes):
            button_brush = QPushButton()
            button_brush.setStyleSheet(BUTTON_BRUSH)
            button_brush.clicked.connect(lambda _, x=i: self.change_brush(x, main_brush))
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
        current_color = QHBoxLayout()
        self.label_preview.setFixedSize(250 - self.size_of_buttons, 40)
        current_color.addWidget(self.label_preview)
        add_color = QPushButton()
        add_color.setFixedSize(self.size_of_buttons, self.size_of_buttons)
        add_color.setStyleSheet(BUTTON_PLUS)
        add_color.clicked.connect(lambda: self.add_color())
        current_color.addWidget(add_color, alignment=Qt.AlignCenter)
        layout.addLayout(current_color)
        layout.addWidget(self.label_visibility)
        layout.addWidget(self.label_palette)
        layout.addWidget(self.label_colors)
        return layout


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PixPad()
    window.show()
    sys.exit(app.exec_())
