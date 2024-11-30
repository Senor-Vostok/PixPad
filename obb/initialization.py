import os
from obb.brush import Brush
from obb.canvas import Canvas


def init_brushes():
    brushes = list()
    for brush in os.listdir("data/brushes"):
        if os.path.isdir(f"data/brushes/{brush}"):
            brushes.append(Brush(f"data/brushes/{brush}/ico.png", None, 'black'))
    return brushes


def init_canvas(size):
    return Canvas(size)
