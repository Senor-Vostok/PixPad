import os
from obb.brush import Brush
from obb.canvas import Canvas
from obb.palette import Palette


def init_brushes():
    brushes = list()
    for brush in os.listdir("data/brushes"):
        if os.path.isdir(f"data/brushes/{brush}"):
            brushes.append(Brush(f"data/brushes/{brush}/ico.png"))
    return brushes


def init_canvas(size):
    return Canvas(size)


def init_palette():
    return Palette(None, None, (94, 128, 19, 120))
