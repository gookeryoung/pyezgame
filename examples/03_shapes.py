"""03_shapes.py - Shape Gallery

Show the main shape drawing APIs, including ellipse drawing and
ARGB alpha blending for primitive colors.
Learn: set_pixel, draw_line, draw_rect, fill_rect, draw_circle,
       fill_circle, draw_ellipse, fill_ellipse, draw_triangle,
       fill_triangle, COLOR_ARGB
"""
import math
import pyezgame as g


def draw_checkerboard(game, x, y, w, h, cell):
    py_ = 0
    while py_ < h:
        px = 0
        while px < w:
            dark = (((px // cell) + (py_ // cell)) & 1) != 0
            color = g.COLOR_RGB(55, 65, 80) if dark else g.COLOR_RGB(85, 95, 110)
            cell_w = min(cell, w - px)
            cell_h = min(cell, h - py_)
            game.fill_rect(x + px, y + py_, cell_w, cell_h, color)
            px += cell
        py_ += cell


def main():
    game = g.GameLib()
    game.open(640, 480, "03 - Shapes and Alpha", True)

    while not game.is_closed():
        t = game.get_time()
        swing = int(math.sin(t * 2.0) * 20.0)

        game.clear(g.COLOR_RGB(24, 28, 36))

        game.draw_text(16, 10, "03 - Shapes, Ellipses and Primitive Alpha", g.COLOR_WHITE)
        game.draw_text(16, 22, "ESC: Quit", g.COLOR_LIGHT_GRAY)

        # Panel 1: SetPixel + DrawLine
        game.draw_text(20, 44, "Pixels + Lines", g.COLOR_WHITE)
        game.draw_rect(16, 58, 192, 144, g.COLOR_LIGHT_GRAY)
        game.fill_rect(20, 62, 88, 88, g.COLOR_RGB(15, 18, 24))
        for py_ in range(88):
            for px in range(88):
                if ((px + py_) % 11) == 0:
                    game.set_pixel(20 + px, 62 + py_,
                                   g.COLOR_RGB(80 + (px * 2) % 175,
                                               80 + (py_ * 2) % 175,
                                               220))
        game.fill_rect(120, 62, 76, 88, g.COLOR_RGB(18, 22, 30))
        for i in range(10):
            y = 70 + i * 7
            game.draw_line(124, 106 + swing // 2, 188, y,
                           g.COLOR_ARGB(255, 255 - i * 18, 90 + i * 12, 80 + i * 10))
        game.draw_line(124, 146, 188, 76, g.COLOR_ARGB(110, 255, 255, 255))
        game.draw_text(26, 162, "SetPixel pattern", g.COLOR_LIGHT_GRAY)
        game.draw_text(26, 174, "DrawLine fan", g.COLOR_LIGHT_GRAY)

        # Panel 2: Rectangles + alpha blending
        game.draw_text(224, 44, "Rectangles + Alpha", g.COLOR_WHITE)
        game.draw_rect(220, 58, 192, 144, g.COLOR_LIGHT_GRAY)
        draw_checkerboard(game, 224, 62, 184, 136, 16)
        game.draw_rect(236, 76, 74, 52, g.COLOR_RED)
        game.draw_rect(252, 92, 74, 52, g.COLOR_ARGB(120, 80, 255, 120))
        game.fill_rect(326, 76, 58, 58, g.COLOR_ARGB(255, 70, 120, 255))
        game.fill_rect(346, 96, 58, 58, g.COLOR_ARGB(120, 255, 210, 50))
        game.draw_text(232, 162, "DrawRect uses alpha too", g.COLOR_LIGHT_GRAY)
        game.draw_text(232, 174, "FillRect blends over grid", g.COLOR_LIGHT_GRAY)

        # Panel 3: Circles + ellipses
        game.draw_text(428, 44, "Circles + Ellipses", g.COLOR_WHITE)
        game.draw_rect(424, 58, 200, 144, g.COLOR_LIGHT_GRAY)
        draw_checkerboard(game, 428, 62, 192, 136, 16)
        game.draw_circle(474, 104, 32, g.COLOR_CYAN)
        game.fill_circle(496, 116, 24, g.COLOR_ARGB(140, 255, 80, 160))
        game.draw_ellipse(566, 102, 44, 24, g.COLOR_GOLD)
        game.fill_ellipse(566, 132, 34, 18, g.COLOR_ARGB(135, 80, 220, 255))
        game.draw_text(438, 162, "DrawCircle / FillCircle", g.COLOR_LIGHT_GRAY)
        game.draw_text(438, 174, "DrawEllipse / FillEllipse", g.COLOR_LIGHT_GRAY)

        # Panel 4: Triangles
        game.draw_text(20, 228, "Triangles", g.COLOR_WHITE)
        game.draw_rect(16, 242, 288, 214, g.COLOR_LIGHT_GRAY)
        draw_checkerboard(game, 20, 246, 280, 206, 20)
        game.draw_triangle(52, 284, 26, 430, 128, 418, g.COLOR_GOLD)
        game.fill_triangle(172, 276, 116, 430, 242, 420, g.COLOR_ARGB(150, 120, 220, 255))
        game.fill_triangle(242, 266, 170, 392, 286, 436, g.COLOR_ARGB(110, 255, 120, 80))
        game.draw_text(28, 432, "Outline + layered fill triangles", g.COLOR_LIGHT_GRAY)

        # Panel 5: Combined scene
        game.draw_text(324, 228, "Combined Scene", g.COLOR_WHITE)
        game.draw_rect(320, 242, 304, 214, g.COLOR_LIGHT_GRAY)
        game.fill_rect(324, 246, 296, 206, g.COLOR_RGB(30, 44, 72))
        game.fill_ellipse(470, 292, 94, 48, g.COLOR_ARGB(120, 255, 210, 90))
        game.fill_circle(558, 296, 30, g.COLOR_ARGB(210, 255, 230, 80))
        game.fill_rect(390, 344, 120, 70, g.COLOR_BROWN)
        game.fill_triangle(376, 344, 450, 286, 524, 344, g.COLOR_DARK_RED)
        game.fill_rect(438, 372, 28, 42, g.COLOR_DARK_BLUE)
        game.fill_rect(406, 360, 18, 18, g.COLOR_ARGB(170, 160, 230, 255))
        game.fill_rect(478, 360, 18, 18, g.COLOR_ARGB(170, 160, 230, 255))
        game.draw_ellipse(548, 388, 46, 24, g.COLOR_WHITE)
        game.fill_ellipse(548, 388, 30, 14, g.COLOR_ARGB(120, 255, 255, 255))
        game.draw_text(336, 432, "Opaque and translucent shapes can mix", g.COLOR_LIGHT_GRAY)

        if game.is_key_pressed(g.KEY_ESCAPE):
            break

        game.update()
        game.wait_frame(30)


if __name__ == "__main__":
    main()
