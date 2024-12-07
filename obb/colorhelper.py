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