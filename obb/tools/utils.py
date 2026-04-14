from PIL import Image
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPixmap, QPainter, QPen, QBrush, QColor, QPolygonF


def clamp_point(x, y, width, height):
    return max(0, min(width - 1, x)), max(0, min(height - 1, y))


def event_to_canvas(pos, scale, canvas):
    x = int(pos.x() // scale)
    y = int(pos.y() // scale)
    return clamp_point(x, y, canvas.width, canvas.height)


def bresenham_line(x1, y1, x2, y2):
    points = []
    dx = abs(x2 - x1)
    dy = -abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx + dy
    x, y = x1, y1
    while True:
        points.append((x, y))
        if x == x2 and y == y2:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x += sx
        if e2 <= dx:
            err += dx
            y += sy
    return points


def normalize_rect(start, end):
    x1, y1 = start
    x2, y2 = end
    left, right = sorted((x1, x2))
    top, bottom = sorted((y1, y2))
    return left, top, right, bottom


def rect_border_points(start, end):
    left, top, right, bottom = normalize_rect(start, end)
    points = set()
    for x in range(left, right + 1):
        points.add((x, top))
        points.add((x, bottom))
    for y in range(top, bottom + 1):
        points.add((left, y))
        points.add((right, y))
    return sorted(points)


def square_border_points(start, end):
    x1, y1 = start
    x2, y2 = end
    side = min(abs(x2 - x1), abs(y2 - y1))
    x2 = x1 + side if x2 >= x1 else x1 - side
    y2 = y1 + side if y2 >= y1 else y1 - side
    return rect_border_points((x1, y1), (x2, y2))


def triangle_border_points(start, end):
    left, top, right, bottom = normalize_rect(start, end)
    mid_x = (left + right) // 2
    a = (mid_x, top)
    b = (left, bottom)
    c = (right, bottom)
    points = set(bresenham_line(*a, *b) + bresenham_line(*b, *c) + bresenham_line(*c, *a))
    return sorted(points)


def ellipse_border_points(start, end):
    left, top, right, bottom = normalize_rect(start, end)
    rx = max(1, (right - left) / 2)
    ry = max(1, (bottom - top) / 2)
    cx = left + rx
    cy = top + ry
    points = set()
    for x in range(left, right + 1):
        for y in range(top, bottom + 1):
            dx = (x - cx) / rx
            dy = (y - cy) / ry
            value = dx * dx + dy * dy
            if 0.82 <= value <= 1.18:
                points.add((x, y))
    if not points:
        points.update(rect_border_points(start, end))
    return sorted(points)


def expand_points(points, thickness):
    thickness = max(1, int(thickness))
    if thickness == 1:
        return sorted(set(points))
    radius = thickness - 1
    expanded = set()
    for x, y in points:
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                expanded.add((x + dx, y + dy))
    return sorted(expanded)


def clip_points(points, canvas):
    return [(x, y) for x, y in points if 0 <= x < canvas.width and 0 <= y < canvas.height]


def rectangle_outline(left, top, right, bottom):
    return rect_border_points((left, top), (right, bottom))


def shift_image(image, dx, dy, size, background=(0, 0, 0, 0)):
    shifted = Image.new('RGBA', size, background)
    shifted.paste(image, (dx, dy), image)
    return shifted


def make_icon(kind):
    pixmap = QPixmap(64, 64)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    pen = QPen(QColor(230, 230, 230))
    pen.setWidth(4)
    painter.setPen(pen)
    if kind == 'line':
        painter.drawLine(14, 50, 50, 14)
    elif kind == 'ellipse':
        painter.drawEllipse(QRectF(12, 16, 40, 30))
    elif kind == 'square':
        painter.drawRect(14, 14, 36, 36)
    elif kind == 'triangle':
        painter.drawPolygon(QPolygonF([QPointF(32, 12), QPointF(14, 50), QPointF(50, 50)]))
    elif kind == 'selection':
        pen.setStyle(Qt.DashLine)
        painter.setPen(pen)
        painter.setBrush(QBrush(Qt.NoBrush))
        painter.drawRect(14, 14, 36, 36)
    elif kind == 'move_layers':
        painter.drawRect(14, 18, 28, 24)
        painter.drawLine(42, 30, 52, 30)
        painter.drawLine(48, 24, 54, 30)
        painter.drawLine(48, 36, 54, 30)
    painter.end()
    return pixmap
