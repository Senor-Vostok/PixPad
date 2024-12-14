import os
from obb.Brush.brush import Brush
from obb.Brush.filler import Filler
from obb.Brush.eraser import Eraser
from obb.Brush.pipette import Pipette
from obb.canvas import Canvas
from obb.palette import Palette
from obb.styles import *


def init_brushes():
    brushes = list()
    for brush in os.listdir("data/brushes"):
        if os.path.isdir(f"data/brushes/{brush}"):
            with open(f"data/brushes/{brush}/manifest", mode='rt') as f:
                type_brush = f.read()
                for file in os.listdir(f"data/brushes/{brush}"):
                    if file[-4:] == '.svg':
                        if type_brush == 'brush':
                            brushes.append(Brush(f"data/brushes/{brush}/ico.png", f"data/brushes/{brush}/{file}"))
                        elif type_brush == 'filler':
                            brushes.append(Filler(f"data/brushes/{brush}/ico.png", f"data/brushes/{brush}/{file}"))
                        elif type_brush == 'eraser':
                            brushes.append(Eraser(f"data/brushes/{brush}/ico.png", f"data/brushes/{brush}/{file}"))
                        elif type_brush == 'pipette':
                            brushes.append(Pipette(f"data/brushes/{brush}/ico.png", f"data/brushes/{brush}/{file}"))
                        break

    return brushes


def init_canvas(size):
    return Canvas(size)


def init_palette():
    return Palette(SIMPLE_SHADOW_PALETTE, (94, 128, 19, 255))
