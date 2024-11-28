SCALE = 300
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
        background-color: rgb(<<color>>);
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
        background-color: rgb(<<color>>);
    }
    QPushButton:hover {
        background-image: url('data/ico/buttons_hover/dark.png');
    }
"""
