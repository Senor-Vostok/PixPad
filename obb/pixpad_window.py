import sys
from PIL import Image
from PyQt5.QtWidgets import (
    QWidget, QGraphicsDropShadowEffect, QGridLayout, QLabel, QShortcut, QScrollArea,
    QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QMenu, QAction, QSlider, QSplitter,
    QFileDialog, QMessageBox, QApplication, QSplashScreen, QGraphicsOpacityEffect
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QTimer
from PyQt5.Qt import QIcon, QColor, QSize, QCursor, QPainter
from PyQt5.QtGui import QKeySequence, QPixmap

from obb.styles import *
from obb.initialization import init_brushes, init_canvas, init_palette
from obb.redefinitions.PixFrame import PixFrame
from obb.redefinitions.PixLabel import PixLabel
from obb.redefinitions.PalLabel import PalLabel
from obb.savefile import PixelEditorSaver
from obb.Windows.create_canvas import ImageSizeWindow
from obb.tools.selection import SelectionTool


class PixPad(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PixPad')
        self.setWindowIcon(QIcon('data/logo/ico.ico'))

        self.size_of_buttons = 30
        self.speed_zoom = 2
        self.shadow_effect = QGraphicsDropShadowEffect(self)
        self.grid_layout = QGridLayout()
        self.brushes = init_brushes()
        self.current_tool = self.brushes[0]
        self.selection_tool = next((tool for tool in self.brushes if isinstance(tool, SelectionTool)), None)
        self.canvas = init_canvas((96, 54))
        self.selected_layers = {self.canvas.current_layer}
        self.layer_button_groups = {}
        self.pixmap_canvas = self.canvas.get_content()

        self.palette = init_palette()
        self.label_preview = QLabel()
        self.label_preview.setPixmap(self.palette.preview())
        self.label_visibility = PalLabel(self, 'visibility')
        self.label_visibility.setPixmap(self.palette.visibility_line())
        self.label_palette = PalLabel(self, 'colors')
        self.label_palette.setPixmap(self.palette.colors_line())
        self.label_colors = PalLabel(self, 'palette')
        self.label_colors.setPixmap(self.palette.show_palette())
        self.colors = [
            (0, 0, 0, 255), (34, 32, 52, 255), (69, 40, 60, 255), (102, 57, 49, 255), (143, 86, 59, 255),
            (223, 113, 38, 255), (217, 160, 102, 255), (238, 195, 154, 255), (251, 242, 54, 255),
            (153, 229, 80, 255), (106, 190, 48, 255), (55, 148, 110, 255), (75, 105, 47, 255), (82, 75, 36, 255),
            (50, 60, 57, 255), (63, 63, 116, 255), (48, 96, 130, 255), (91, 110, 225, 255), (99, 155, 255, 255),
            (95, 205, 228, 255), (203, 219, 252, 255), (255, 255, 255, 255), (155, 173, 183, 255), (132, 126, 135, 255),
            (105, 106, 106, 255), (89, 86, 82, 255), (118, 66, 138, 255), (172, 50, 50, 255), (217, 87, 99, 255),
            (215, 123, 186, 255), (143, 151, 74, 255), (138, 111, 48, 255)
        ]
        self.color_grid_layout = QGridLayout()
        self.color_grid_layout.setHorizontalSpacing(3)
        self.color_grid_layout.setVerticalSpacing(3)
        self.show_colors(self.colors)
        self.current_tool.color = self.palette.color

        self.drawing_label = PixLabel(self)
        self.tool_buttons = []
        self.size_window = None

        self.timer_anim = QTimer()
        self.timer_anim.setInterval(100)
        self.timer_anim.timeout.connect(self.play_next_frame)
        self.play_animation = False

        self.init_ui()
        self.showMaximized()

    def init_ui(self):
        self.undo_shortcut = QShortcut(QKeySequence('Ctrl+Z'), self)
        self.undo_shortcut.activated.connect(self.last_image)
        self.deselect_shortcut = QShortcut(QKeySequence('Ctrl+D'), self)
        self.deselect_shortcut.activated.connect(self.clear_all_selections)

        self.shadow_effect.setBlurRadius(20)
        self.shadow_effect.setXOffset(5)
        self.shadow_effect.setYOffset(5)
        self.shadow_effect.setColor(QColor(0, 0, 0, 160))

        self.setStyleSheet('background-color: rgb(51, 51, 51)')
        self.left_scroll_area = QScrollArea(self)
        self.left_scroll_area.setFrameShape(QFrame.StyledPanel)
        self.left_scroll_area.setWidgetResizable(True)
        self.left_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.left_content = QWidget()
        self.choisen_frame = QLabel(self.left_content)
        self.choisen_frame.setStyleSheet('background-color: rgba(255, 255, 255, 50);')
        self.choisen_frame.setFixedSize(2000, self.size_of_buttons + 10)
        self.choisen_frame.lower()
        self.choisen_layer = QLabel(self.left_content)
        self.choisen_layer.setStyleSheet('background-color: rgba(255, 255, 255, 50);')
        self.choisen_layer.setFixedSize(self.size_of_buttons + 10, 2000)
        self.choisen_layer.lower()
        self.left_content.setStyleSheet('background-color: rgb(32, 33, 37);border-radius: 5px;border: 4px solid rgba(0, 0, 0, 255);')
        self.left_layout = QVBoxLayout(self.left_content)
        self.left_layout.setAlignment(Qt.AlignTop)
        self.left_layout.addLayout(self.grid_layout)
        self.left_content.setLayout(self.left_layout)
        self.left_scroll_area.setWidget(self.left_content)
        self.refresh_layer_grid()

        self.center_frame = PixFrame(self.zoom_canvas)
        self.center_frame.setFrameShape(QFrame.StyledPanel)
        self.center_frame.setWidgetResizable(True)
        self.center_frame.setStyleSheet('background-color: rgb(32, 33, 37);border-radius: 5px;border: 4px solid rgba(0, 0, 0, 255);')
        cursor_pixmap = QPixmap(10, 10)
        cursor_pixmap.fill(Qt.transparent)
        painter = QPainter(cursor_pixmap)
        painter.setBrush(Qt.white)
        painter.drawEllipse(2, 2, 6, 6)
        painter.end()
        self.center_frame.setCursor(QCursor(cursor_pixmap))
        self.update_canvas()
        self.center_frame.setAlignment(Qt.AlignCenter)
        self.center_frame.setWidget(self.drawing_label)

        self.right_panel = QFrame(self)
        self.right_panel.setStyleSheet('background-color: rgb(32, 33, 37);border-radius: 5px;border: 4px solid rgba(0, 0, 0, 255);')
        self.right_panel.setFrameShape(QFrame.StyledPanel)
        self.right_layout = QVBoxLayout(self.right_panel)
        self.right_layout.addLayout(self.show_brushes(self.brushes))
        self.colors_layout = QVBoxLayout(self.right_panel)
        self.colors_layout.setAlignment(Qt.AlignTop)
        self.colors_layout.addLayout(self.color_grid_layout)
        self.right_layout.addLayout(self.colors_layout, 6)
        self.right_layout.addLayout(self.show_palette())

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.left_scroll_area)
        self.splitter.addWidget(self.center_frame)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 18)

        self.top_panel = QHBoxLayout()
        self.build_menus()
        self.top_panel.addWidget(self.file)
        self.top_panel.addWidget(self.layer)
        self.top_panel.addWidget(self.frame)
        self.top_panel.addWidget(self.palitra)
        self.top_panel.addWidget(self.animation_button)
        self.top_panel.addWidget(self.slider)
        self.top_panel.addWidget(self.value_brush)
        self.top_panel.setAlignment(Qt.AlignLeft)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addLayout(self.top_panel, 1)
        self.work_layout = QHBoxLayout(self)
        self.work_layout.addWidget(self.splitter, 10)
        self.work_layout.addWidget(self.right_panel, 1)
        self.main_layout.addLayout(self.work_layout, 30)

    def build_menus(self):
        self.file = QPushButton('Файл')
        self.file.setStyleSheet(BUTTON_SETTING)
        self.file.setFixedWidth(80)
        self.file_menu = QMenu()
        create = QAction('Новый...', self)
        create.triggered.connect(self.create_new_canvas)
        open_ = QAction('Открыть...', self)
        open_.triggered.connect(self.open_canvas)
        save_png_action = QAction('Сохранить как PNG...', self)
        save_png_action.triggered.connect(self.save_canvas_as_png)
        save_jpeg_action = QAction('Сохранить как JPEG...', self)
        save_jpeg_action.triggered.connect(self.save_canvas_as_jpeg)
        save_gif_action = QAction('Сохранить как GIF...', self)
        save_gif_action.triggered.connect(self.save_canvas_as_gif)
        self.file_menu.addActions([create, open_, save_png_action, save_jpeg_action, save_gif_action])
        self.file.setMenu(self.file_menu)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(32)
        self.slider.setTickInterval(1)
        self.slider.setFixedWidth(128)
        self.slider.valueChanged.connect(self.resize_brush)
        self.value_brush = QLabel(f'X {self.slider.value()}')
        self.value_brush.setStyleSheet(LABEL_INFO)
        self.value_brush.setFixedWidth(64)

        self.animation_button = QPushButton()
        self.animation_button.clicked.connect(self.animation_canvas)
        self.animation_button.setFixedSize(self.size_of_buttons, self.size_of_buttons)
        self.animation_button.setStyleSheet(BUTTON_PLAY)

        self.layer = QPushButton('Слой')
        self.layer.setStyleSheet(BUTTON_SETTING)
        self.layer.setFixedWidth(80)
        self.layer_menu = QMenu()
        layer_new = QAction('Новый...', self)
        layer_new.triggered.connect(self.add_layout)
        hide_show = QAction('Скрыть/показать', self)
        hide_show.triggered.connect(lambda: self.hide_show_layer(self.canvas.current_layer))
        delete = QAction('Удалить...', self)
        delete.triggered.connect(self.delete_layout)
        self.layer_menu.addActions([layer_new, hide_show, delete])
        self.layer.setMenu(self.layer_menu)

        self.frame = QPushButton('Кадр')
        self.frame.setStyleSheet(BUTTON_SETTING)
        self.frame.setFixedWidth(80)
        self.frame_menu = QMenu()
        frame_new = QAction('Новый...', self)
        frame_new.triggered.connect(self.add_frame)
        frame_delete = QAction('Удалить...', self)
        frame_delete.triggered.connect(self.delete_frame)
        self.frame_menu.addActions([frame_new, frame_delete])
        self.frame.setMenu(self.frame_menu)

        self.palitra = QPushButton('Палитра')
        self.palitra.setStyleSheet(BUTTON_SETTING)
        self.palitra.setFixedWidth(80)
        self.palitra_menu = QMenu()
        simple = QAction('Тень', self)
        simple.triggered.connect(lambda: self.change_palette(SIMPLE_SHADOW_PALETTE))
        shadow = QAction('Тень пиксель-арт', self)
        shadow.triggered.connect(lambda: self.change_palette(PIXEL_SHADOW_PALETTE))
        normals = QAction('Нормаль', self)
        normals.triggered.connect(lambda: self.change_palette(NORMAL_PALETTE, 'normal'))
        self.palitra_menu.addActions([simple, shadow, normals])
        self.palitra.setMenu(self.palitra_menu)

    def play_next_frame(self):
        next_frame = (self.canvas.current_frame + 1) % len(self.canvas.layers[0].frames)
        self.change_frame(next_frame + 1, self.canvas.current_layer)

    def clear_selection(self):
        self.canvas.clear_preview(update=False)
        if self.selection_tool:
            self.selection_tool.clear_selection(self.canvas)
        else:
            self.canvas.clear_overlay_border()
        self.update_canvas()

    def clear_layer_selection(self, keep_current=False):
        self.selected_layers = {self.canvas.current_layer} if keep_current else set()
        self.refresh_layer_grid()

    def clear_all_selections(self):
        self.clear_selection()
        self.clear_layer_selection()

    def _selected_style(self, base_style):
        return base_style.replace('border: none;', 'border: 2px solid rgb(95, 205, 228); background-color: rgba(95, 205, 228, 35);')

    def _layer_header_style(self, layer_index):
        base = BUTTON_LAYOUT if self.canvas.layers[layer_index].is_active else BUTTON_LAYOUT_D
        return self._selected_style(base) if layer_index in self.selected_layers else base

    def _frame_style(self, layer_index):
        selected_style = globals().get("BUTTON_FRAME_SELECTED", BUTTON_FRAME)
        return selected_style if layer_index in self.selected_layers else BUTTON_FRAME

    def _normalize_selected_layers(self):
        self.selected_layers = {index for index in self.selected_layers if 0 <= index < len(self.canvas.layers)}

    def _select_layers_from_click(self, layer_index):
        modifiers = QApplication.keyboardModifiers()
        if modifiers & Qt.ControlModifier:
            if layer_index in self.selected_layers:
                self.selected_layers.remove(layer_index)
            else:
                self.selected_layers.add(layer_index)
        else:
            self.selected_layers = {layer_index}
        self._normalize_selected_layers()

    def on_layer_header_clicked(self, layer_index):
        self.clear_selection()
        self.canvas.current_layer = layer_index
        self._select_layers_from_click(layer_index)
        self.refresh_layer_grid()
        self.update_canvas()

    def on_layer_frame_clicked(self, layer_index, frame_index):
        self.clear_selection()
        self.canvas.current_layer = layer_index
        self.canvas.current_frame = frame_index
        self._select_layers_from_click(layer_index)
        self.canvas.update_canvas()
        self.update_canvas()
        self.refresh_layer_grid()

    def on_layer_visibility_toggle(self, layer_index):
        self.hide_show_layer(layer_index)

    def change_palette(self, pattern_palette, type_palette=None):
        self.palette = type(self.palette)(pattern_palette, self.palette.color, type_palette)
        self.label_preview.setPixmap(self.palette.preview())
        self.label_visibility.setPixmap(self.palette.visibility_line())
        self.label_palette.setPixmap(self.palette.colors_line())
        self.label_colors.setPixmap(self.palette.show_palette())
        self.current_tool.color = self.palette.color

    def last_image(self):
        if self.canvas.undo():
            self.update_canvas()
            self.refresh_layer_grid()

    def animation_canvas(self):
        self.play_animation = not self.play_animation
        self.animation_button.setStyleSheet(BUTTON_PAUSE if self.play_animation else BUTTON_PLAY)
        if self.play_animation:
            self.timer_anim.start()
        else:
            self.timer_anim.stop()

    def move_visualiser(self):
        self.choisen_layer.move(4 + self.canvas.current_layer * (self.size_of_buttons + 10), 0)
        self.choisen_frame.move(0, 4 + (self.canvas.current_frame + 1) * (self.size_of_buttons + 5))

    def open_canvas(self):
        options = QFileDialog.Options()
        filepath, _ = QFileDialog.getOpenFileName(self, 'Открыть', '', 'PNG Files (*.png)', options=options)
        if not filepath:
            return
        image = Image.open(filepath).convert('RGBA')
        if image.width * image.height >= SCALE_WARNING:
            QMessageBox.warning(self, 'Большое разрешение', WARNING_SCALE)
        self.canvas = init_canvas((image.width, image.height))
        self.selected_layers = {self.canvas.current_layer}
        self.canvas.set_current_image(image.copy())
        self.pixmap_canvas = self.canvas.get_content()
        self.clear_selection()
        self.update_canvas()
        self.refresh_layer_grid()

    def refresh_layer_grid(self):
        self._normalize_selected_layers()
        self.layer_button_groups = {}
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self.show_lf(len(self.canvas.layers), len(self.canvas.layers[0].frames))
        self.move_visualiser()

    def create_new_canvas(self):
        self.size_window = ImageSizeWindow(self.create_canvas)
        self.size_window.show()

    def create_canvas(self, size):
        self.canvas = init_canvas(size)
        self.selected_layers = {self.canvas.current_layer}
        self.pixmap_canvas = self.canvas.get_content()
        self.clear_selection()
        self.update_canvas()
        self.refresh_layer_grid()

    def change_tool(self, number, label):
        self.canvas.clear_preview()
        self.current_tool = self.brushes[number]
        self.current_tool.color = self.palette.color
        label.setPixmap(self.current_tool.get_ico([100, 100]))
        self.slider.setSliderPosition(getattr(self.current_tool, 'size', 1))

    def resize_brush(self):
        self.current_tool.resize(self.slider.value())
        self.value_brush.setText(f'X{self.slider.value()}')

    def _build_saver(self):
        pil_image = self.canvas.get_raw()
        return PixelEditorSaver(self.canvas.width, self.canvas.height, self.canvas.background_color, pil_image, self.canvas)

    def save_canvas_as_png(self):
        options = QFileDialog.Options()
        filepath, _ = QFileDialog.getSaveFileName(self, 'Сохранить как PNG', '', 'PNG Files (*.png)', options=options)
        if filepath:
            self._build_saver().save_as_png(filepath)

    def save_canvas_as_jpeg(self):
        options = QFileDialog.Options()
        filepath, _ = QFileDialog.getSaveFileName(self, 'Сохранить как JPEG', '', 'JPEG Files (*.jpeg;*.jpg)', options=options)
        if filepath:
            self._build_saver().save_as_jpeg(filepath)

    def save_canvas_as_gif(self):
        options = QFileDialog.Options()
        filepath, _ = QFileDialog.getSaveFileName(self, 'Сохранить как GIF', '', 'GIF Files (*.gif)', options=options)
        if filepath:
            self._build_saver().save_as_gif(filepath)

    def show_lf(self, count_layouts=1, count_frames=1):
        self.grid_layout.setHorizontalSpacing(10)
        self.grid_layout.setVerticalSpacing(5)
        for i in range(count_layouts):
            self.layer_button_groups[i] = []
            layout_button = QPushButton()
            layout_button.setStyleSheet(self._layer_header_style(i))
            layout_button.setToolTip('ЛКМ — выбрать слой, Ctrl+ЛКМ — добавить к выделению, ПКМ — скрыть/показать')
            layout_button.setContextMenuPolicy(Qt.CustomContextMenu)
            layout_button.customContextMenuRequested.connect(lambda _, x=i: self.on_layer_visibility_toggle(x))
            layout_button.setFixedSize(self.size_of_buttons, self.size_of_buttons)
            layout_button.clicked.connect(lambda _, x=i: self.on_layer_header_clicked(x))
            self.grid_layout.addWidget(layout_button, 0, i)
            self.layer_button_groups[i].append(layout_button)
            for j in range(count_frames):
                frame_button = QPushButton()
                frame_button.setStyleSheet(self._frame_style(i))
                frame_button.setFixedSize(self.size_of_buttons, self.size_of_buttons)
                frame_button.clicked.connect(lambda _, x=i, y=j: self.on_layer_frame_clicked(x, y))
                self.grid_layout.addWidget(frame_button, j + 1, i)
                self.layer_button_groups[i].append(frame_button)
                if i == count_layouts - 1 and j == count_frames - 1:
                    plus_frame = QPushButton()
                    plus_frame.setStyleSheet(BUTTON_PLUS)
                    plus_frame.setFixedSize(self.size_of_buttons, self.size_of_buttons)
                    plus_frame.clicked.connect(self.add_frame)
                    self.grid_layout.addWidget(plus_frame, j + 2, 0)
            if i == count_layouts - 1:
                plus_layer = QPushButton()
                plus_layer.setStyleSheet(BUTTON_PLUS)
                plus_layer.setFixedSize(self.size_of_buttons, self.size_of_buttons)
                plus_layer.clicked.connect(self.add_layout)
                self.grid_layout.addWidget(plus_layer, 0, i + 1)

    def hide_show_layer(self, number_layer):
        self.clear_selection()
        self.canvas.layers[number_layer].is_active = not self.canvas.layers[number_layer].is_active
        self.canvas.update_canvas()
        self.update_canvas()
        self.refresh_layer_grid()

    def change_color(self, color):
        self.palette.color = color
        self.current_tool.color = color
        self.label_palette.setPixmap(self.palette.colors_line())
        self.label_colors.setPixmap(self.palette.show_palette(create_new=True))
        self.label_visibility.setPixmap(self.palette.visibility_line())
        self.label_preview.setPixmap(self.palette.preview())

    def add_color(self):
        max_columns = 8
        color = self.palette.color
        color_button = QPushButton()
        color_button.setFixedSize(self.size_of_buttons, self.size_of_buttons)
        brightness = sum(color[:3]) / 3
        if brightness <= 128:
            color_button.setStyleSheet(BUTTON_BRIGHT.split('<<color>>')[0] + ', '.join(str(j) for j in color) + BUTTON_BRIGHT.split('<<color>>')[1])
        else:
            color_button.setStyleSheet(BUTTON_DARK.split('<<color>>')[0] + ', '.join(str(j) for j in color) + BUTTON_DARK.split('<<color>>')[1])
        color_button.clicked.connect(lambda _, c=color: self.change_color(c))
        row = len(self.colors) // max_columns
        col = len(self.colors) % max_columns
        self.color_grid_layout.addWidget(color_button, row, col)
        self.colors.append(color)

    def change_frame(self, number_frame, number_layer):
        self.clear_selection()
        self.canvas.current_layer = number_layer
        self.canvas.current_frame = number_frame - 1
        self.canvas.update_canvas()
        self.update_canvas()
        self.refresh_layer_grid()

    def add_frame(self):
        self.clear_selection()
        self._normalize_selected_layers()
        self.canvas.add_frame()
        self.refresh_layer_grid()
        self.update_canvas()

    def delete_frame(self):
        self.clear_selection()
        self._normalize_selected_layers()
        if len(self.canvas.layers[0].frames) == 1:
            QMessageBox.warning(self, 'Отклонено', 'Вы не можете удалить единственный кадр')
            return
        self.canvas.delete_frame(self.canvas.current_frame)
        self.update_canvas()
        self.refresh_layer_grid()

    def add_layout(self):
        self.clear_selection()
        self.canvas.add_layout()
        self.selected_layers = {len(self.canvas.layers) - 1}
        self.refresh_layer_grid()
        self.update_canvas()

    def delete_layout(self):
        self.clear_selection()
        if len(self.canvas.layers) == 1:
            QMessageBox.warning(self, 'Отклонено', 'Вы не можете удалить единственный слой')
            return
        removed = self.canvas.current_layer
        self.canvas.delete_layout(removed)
        self.selected_layers = {index for index in self.selected_layers if index != removed}
        self.selected_layers = {index - 1 if index > removed else index for index in self.selected_layers}
        if not self.selected_layers and self.canvas.layers:
            self.selected_layers = {self.canvas.current_layer}
        self.update_canvas()
        self.refresh_layer_grid()

    def update_canvas(self, width=None, height=None):
        if width is None or height is None:
            width, height = self.pixmap_canvas.width(), self.pixmap_canvas.height()
        self.pixmap_canvas = self.canvas.get_content().scaled(width, height, Qt.KeepAspectRatio)
        self.drawing_label.setFixedSize(self.pixmap_canvas.width(), self.pixmap_canvas.height())
        self.drawing_label.setPixmap(self.pixmap_canvas)

    def zoom_canvas(self, delta):
        if delta > 0:
            width = self.pixmap_canvas.width() * self.speed_zoom
            height = self.pixmap_canvas.height() * self.speed_zoom
        else:
            width = max(self.canvas.width, self.pixmap_canvas.width() // self.speed_zoom)
            height = max(self.canvas.height, self.pixmap_canvas.height() // self.speed_zoom)
        self.update_canvas(width, height)

    def show_colors(self, colors):
        max_columns = 8
        for i, color in enumerate(colors):
            color_button = QPushButton()
            color_button.setFixedSize(self.size_of_buttons, self.size_of_buttons)
            brightness = sum(color[:3]) / 3
            if brightness <= 128:
                color_button.setStyleSheet(BUTTON_BRIGHT.split('<<color>>')[0] + ', '.join(str(j) for j in color) + BUTTON_BRIGHT.split('<<color>>')[1])
            else:
                color_button.setStyleSheet(BUTTON_DARK.split('<<color>>')[0] + ', '.join(str(j) for j in color) + BUTTON_DARK.split('<<color>>')[1])
            color_button.clicked.connect(lambda _, c=color: self.change_color(c))
            row = i // max_columns
            col = i % max_columns
            self.color_grid_layout.addWidget(color_button, row, col)

    def show_brushes(self, brushes):
        brushes_layout = QHBoxLayout()
        brushes_layout.setAlignment(Qt.AlignLeft)
        main_brush = QLabel(self)
        main_brush.setFixedSize(100, 100)
        main_brush.setPixmap(self.current_tool.get_ico([100, 100]))
        main_brush.setAlignment(Qt.AlignCenter)
        brushes_layout.addWidget(main_brush)
        grid_brush = QGridLayout()
        grid_brush.setHorizontalSpacing(0)
        grid_brush.setVerticalSpacing(0)
        max_column = 4
        size_of_buttons = int(self.size_of_buttons * 1.2)
        for i, brush in enumerate(brushes):
            button_brush = QPushButton()
            button_brush.setStyleSheet(BUTTON_BRUSH)
            button_brush.clicked.connect(lambda _, x=i: self.change_tool(x, main_brush))
            button_brush.setFixedSize(size_of_buttons, size_of_buttons)
            button_brush.setIcon(QIcon(brush.get_ico()))
            button_brush.setIconSize(QSize(int(size_of_buttons * 0.75), int(size_of_buttons * 0.75)))
            row = i // max_column
            col = i % max_column
            grid_brush.addWidget(button_brush, row, col)
            self.tool_buttons.append(button_brush)
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
        add_color.clicked.connect(self.add_color)
        current_color.addWidget(add_color, alignment=Qt.AlignCenter)
        layout.addLayout(current_color)
        layout.addWidget(self.label_visibility)
        layout.addWidget(self.label_palette)
        layout.addWidget(self.label_colors)
        return layout

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Выход', 'Вы уверены, что хотите выйти?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class AnimatedSplashScreen(QSplashScreen):
    def __init__(self, pixmap):
        super().__init__(pixmap)
        self.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b'opacity')

    def fade_in(self):
        self.animation.setDuration(1000)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.start()

    def fade_out(self, callback):
        self.animation.setDuration(500)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.finished.connect(callback)
        self.animation.start()


def run_app():
    app = QApplication(sys.argv)
    splash_pix = QPixmap('data/logo/logo.png')
    splash = AnimatedSplashScreen(splash_pix)
    splash.show()
    splash.fade_in()

    def start_main_window():
        splash.close()
        window = PixPad()
        window.show()

    QTimer.singleShot(1500, lambda: splash.fade_out(start_main_window))
    sys.exit(app.exec_())
