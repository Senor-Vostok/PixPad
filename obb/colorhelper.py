import math


def blend_pixels(pixel_top, pixel_bottom):
    r1, g1, b1, a1 = pixel_top
    r2, g2, b2, a2 = pixel_bottom
    alpha1 = a1 / 255.0
    alpha2 = a2 / 255.0
    alpha = alpha1 + alpha2 * (1 - alpha1)
    if alpha == 0:
        return 0, 0, 0, 0
    r = int((r1 * alpha1 + r2 * alpha2 * (1 - alpha1)) / alpha)
    g = int((g1 * alpha1 + g2 * alpha2 * (1 - alpha1)) / alpha)
    b = int((b1 * alpha1 + b2 * alpha2 * (1 - alpha1)) / alpha)
    a = int(alpha * 255)
    return r, g, b, a


def find_closest_color(data, width, height, target_color):
    min_distance = float('inf')
    closest_x, closest_y = 0, 0
    target_brightness = 0.299 * target_color[0] + 0.587 * target_color[1] + 0.114 * target_color[2]
    for x in range(width):
        for y in range(height):
            color = data[x, y]
            color_brightness = 0.299 * color[0] + 0.587 * color[1] + 0.114 * color[2]
            distance = sum((color[i] - target_color[i]) ** 2 for i in range(3)) + (
                        color_brightness - target_brightness) ** 2

            if distance < min_distance:
                min_distance = distance
                closest_x, closest_y = x, y

    return closest_x, closest_y


def adjust_color_based_on_brightness(color):
    brightness = 0.299 * color[0] + 0.587 * color[1] + 0.114 * color[2]
    threshold = 1
    return (0, 0, 0, color[3]) if brightness > threshold else (255, 255, 255, color[3])


def draw_border_circle(line, width, height, center, radius=6, border_width=2):
    cx, cy = center
    for y in range(max(0, cy - radius), min(height, cy + radius + 1)):
        for x in range(max(0, cx - radius), min(width, cx + radius + 1)):
            dist_sq = (x - cx) ** 2 + (y - cy) ** 2
            if radius ** 2 >= dist_sq >= (radius - border_width) ** 2:
                line[x, y] = adjust_color_based_on_brightness(line[x, y])


def project_point_on_line(x, y, x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    if dx == 0 and dy == 0:
        return x1, y1
    t = ((x - x1) * dx + (y - y1) * dy) / (dx ** 2 + dy ** 2)
    t = max(0, min(1, t))
    px = x1 + t * dx
    py = y1 + t * dy
    return px, py


def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def interpolate_color(start_color, alpha):
    r, g, b, a = start_color
    a = alpha
    return r, g, b, a


def interpolate_alpha(base_alpha, dist, max_dist):
    fade = max(0, base_alpha - int((dist / max_dist) * 255))
    return fade
