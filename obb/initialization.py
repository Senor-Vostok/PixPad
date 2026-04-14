import os
from obb.Brush.brush import Brush
from obb.Brush.filler import Filler
from obb.Brush.eraser import Eraser
from obb.Brush.pipette import Pipette
from obb.canvas import Canvas
from obb.palette import Palette
from obb.styles import *
from obb.tools.shapes import ShapeTool
from obb.tools.selection import SelectionTool
from obb.tools.layer_move import LayerMoveTool


def init_brushes():
    brushes = []
    brushes_dir = "data/brushes"
    if os.path.isdir(brushes_dir):
        for brush in os.listdir(brushes_dir):
            brush_dir = f"{brushes_dir}/{brush}"
            if os.path.isdir(brush_dir):
                with open(f"{brush_dir}/manifest", mode='rt') as f:
                    type_brush = f.read().strip()
                    for file in os.listdir(brush_dir):
                        if file.endswith('.svg'):
                            ico_path = f"{brush_dir}/ico.png"
                            vector_path = f"{brush_dir}/{file}"
                            if type_brush == 'brush':
                                brushes.append(Brush(ico_path, vector_path))
                            elif type_brush == 'filler':
                                brushes.append(Filler(ico_path, vector_path))
                            elif type_brush == 'eraser':
                                brushes.append(Eraser(ico_path, vector_path))
                            elif type_brush == 'pipette':
                                brushes.append(Pipette(ico_path, vector_path))
                            break

    brushes.extend([
        ShapeTool('Линия', 'line'),
        ShapeTool('Эллипс', 'ellipse'),
        ShapeTool('Квадрат', 'square'),
        ShapeTool('Треугольник', 'triangle'),
        SelectionTool(),
        LayerMoveTool(),
    ])
    return brushes


def init_canvas(size):
    return Canvas(size)


def init_palette():
    return Palette(SIMPLE_SHADOW_PALETTE, (163, 73, 164, 255))
