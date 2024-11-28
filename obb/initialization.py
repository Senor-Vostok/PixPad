import os
from obb.brush import Brush


def init_brushes():
    brushes = list()
    for brush in os.listdir("data/brushes"):
        if os.path.isdir(f"data/brushes/{brush}"):
            brushes.append(Brush(f"data/brushes/{brush}/ico.png", None, 'black'))
    return brushes
