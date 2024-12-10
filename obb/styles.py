SCALE = 300
WARNING_SCALE = "Изображение слишком большого формата\nмогут быть перебои в работе"
SCALE_WARNING = 240000
BUTTON_PLAY = """
    QPushButton {
        background-image: url('data/ico/buttons_passive/play.png');
        background-repeat: no-repeat;
        background-position: center;
        border-radius: 5px;
        border: 4px;
    }
    QPushButton:hover {
        background-image: url('data/ico/buttons_hover/play.png');
    }
    QPushButton:pressed {
        background-image: url('data/ico/buttons_active/play.png');
    }
"""
BUTTON_PAUSE = """
    QPushButton {
        background-image: url('data/ico/buttons_passive/pause.png');
        background-repeat: no-repeat;
        background-position: center;
        border-radius: 5px;
        border: 4px;
    }
    QPushButton:hover {
        background-image: url('data/ico/buttons_hover/pause.png');
    }
    QPushButton:pressed {
        background-image: url('data/ico/buttons_active/pause.png');
    }
"""
BUTTON_LAYOUT = """
    QPushButton {
        background-image: url('data/ico/buttons_passive/layout.png');
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QPushButton:hover {
        background-image: url('data/ico/buttons_hover/layout.png');
    }
    QPushButton:pressed {
        background-image: url('data/ico/buttons_active/layout.png');
    }
"""
BUTTON_LAYOUT_D = """
    QPushButton {
        background-image: url('data/ico/buttons_passive/layout_hide.png');
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QPushButton:hover {
        background-image: url('data/ico/buttons_hover/layout_hide.png');
    }
    QPushButton:pressed {
        background-image: url('data/ico/buttons_active/layout_hide.png');
    }
"""
BUTTON_PLUS = """
    QPushButton {
        background-image: url('data/ico/buttons_passive/plus.png');
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QPushButton:hover {
        background-image: url('data/ico/buttons_hover/plus.png');
    }
    QPushButton:pressed {
        background-image: url('data/ico/buttons_active/plus.png');
    }
"""
BUTTON_FRAME_SELECTED = """
    QPushButton {
        background-image: url('data/ico/buttons_passive/frame_selected.png');
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QPushButton:hover {
        background-image: url('data/ico/buttons_hover/frame_selected.png');
    }
    QPushButton:pressed {
        background-image: url('data/ico/buttons_active/frame_selected.png');
    }
"""
BUTTON_FRAME = """
    QPushButton {
        background-image: url('data/ico/buttons_passive/frame.png');
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QPushButton:hover {
        background-image: url('data/ico/buttons_hover/frame.png');
    }
    QPushButton:pressed {
        background-image: url('data/ico/buttons_active/frame.png');
    }
"""
BUTTON_BRIGHT = """
    QPushButton {
        background-repeat: no-repeat;
        background-position: center;
        border: none;
        background-color: rgba(<<color>>);
    }
    QPushButton:hover {
        background-image: url('data/ico/buttons_hover/bright.png');
    }
"""
BUTTON_DARK = """
    QPushButton {
        background-repeat: no-repeat;
        background-position: center;
        border: none;
        background-color: rgba(<<color>>);
    }
    QPushButton:hover {
        background-image: url('data/ico/buttons_hover/dark.png');
    }
"""
BUTTON_BRUSH = """
    QPushButton {
        background-repeat: no-repeat;
        background-position: center;
        border: none;
        
    }
    QPushButton:hover {
        background-image: url('data/ico/buttons_hover/dark.png');
    }
    QPushButton:pressed {
        background-image: url('data/ico/buttons_hover/bright.png');
    }
"""