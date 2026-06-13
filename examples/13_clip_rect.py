"""13_clip_rect.py - Clip Rectangle Demo

Demonstrates set_clip / clear_clip / get_clip to restrict drawing to sub-regions.
Three clip windows on screen:
  - Shape window: lines, circles, triangles clipped at the boundary
  - Text window: scrolling text clipped by set_clip
  - Sprite window: code-generated sprite + scaled copies clipped

Learn: set_clip, clear_clip, get_clip, how all draw calls respect clip
"""

import math

import pyezgame as g


def create_star_sprite(game):
    sid = game.create_sprite(16, 16)
    if sid < 0:
        return -1
    for y in range(16):
        for x in range(16):
            game.set_sprite_pixel(sid, x, y, 0x00000000)
    for i in range(16):
        game.set_sprite_pixel(sid, 8, i, g.COLOR_YELLOW)
        game.set_sprite_pixel(sid, i, 8, g.COLOR_YELLOW)
        game.set_sprite_pixel(sid, i, i, g.COLOR_GOLD)
        game.set_sprite_pixel(sid, 15 - i, i, g.COLOR_GOLD)
    for dy in range(6, 11):
        for dx in range(6, 11):
            game.set_sprite_pixel(sid, dx, dy, g.COLOR_WHITE)
    return sid


def draw_window_border(game, x, y, w, h, title, border_color) -> None:
    game.draw_rect(x - 1, y - 1, w + 2, h + 2, border_color)
    game.draw_text(x + 6, y + 4, title, g.COLOR_WHITE)


def main() -> None:
    game = g.GameLib()
    game.open(640, 480, "13 - Clip Rectangle Demo", True)

    star = create_star_sprite(game)

    # Window regions
    w1x, w1y, w1w, w1h = 20, 30, 280, 200  # Shapes
    w2x, w2y, w2w, w2h = 330, 30, 290, 200  # Text
    w3x, w3y, w3w, w3h = 20, 260, 600, 190  # Sprites

    while not game.is_closed():
        if game.is_key_pressed(g.KEY_ESCAPE):
            break
        t = game.get_time()

        game.clear(g.COLOR_RGB(18, 20, 28))
        game.draw_text(20, 8, "13_clip_rect: SetClip restricts all drawing to sub-regions", g.COLOR_LIGHT_GRAY)

        # === Window 1: Shapes ===
        game.set_clip(w1x, w1y, w1w, w1h)
        game.fill_rect(w1x, w1y, w1w, w1h, g.COLOR_RGB(26, 36, 52))

        game.fill_triangle(
            w1x + w1w // 2,
            w1y - 30,
            w1x + w1w + 60,
            w1y + w1h + 20,
            w1x - 60,
            w1y + w1h + 20,
            g.COLOR_ARGB(100, 255, 180, 40),
        )

        for i in range(6):
            sweep = (int(t * 120.0) + i * 50) % (w1w + 140)
            x0 = w1x - 70 + sweep
            game.draw_line(x0, w1y - 10, x0 + 100, w1y + w1h + 20, g.COLOR_ARGB(180, 120 + i * 22, 220 - i * 26, 255))

        cx = w1x + w1w // 2 + int(math.cos(t * 1.7) * (w1w // 2 + 30))
        cy = w1y + w1h // 2 + int(math.sin(t * 2.1) * (w1h // 2 - 10))
        game.fill_circle(cx, cy, 28, g.COLOR_ARGB(200, 255, 90, 120))

        game.draw_ellipse(w1x + w1w // 2, w1y + w1h // 2, w1w // 2 + 40, w1h // 3, g.COLOR_CYAN)

        game.clear_clip()
        draw_window_border(game, w1x, w1y, w1w, w1h, "Shape Clip", g.COLOR_WHITE)

        # === Window 2: Text ===
        game.set_clip(w2x, w2y, w2w, w2h)
        game.fill_rect(w2x, w2y, w2w, w2h, g.COLOR_RGB(44, 30, 22))

        marquee_x = w2x + w2w - (int(t * 100.0) % (w2w + 400))
        game.draw_text(marquee_x, w2y + 30, "This text scrolls and is clipped at the window boundary...", g.COLOR_GOLD)

        osc_x = w2x - 80 + (int(t * 60.0) % (w2w + 160))
        game.draw_text(osc_x, w2y + 60, "DrawText is also clipped!", g.COLOR_WHITE)

        clip_info = game.get_clip()
        game.draw_printf(
            w2x + 8,
            w2y + 100,
            g.COLOR_LIGHT_GRAY,
            f"GetClip: {clip_info[0]},{clip_info[1]} {clip_info[2]}x{clip_info[3]}",
        )
        game.draw_printf(w2x + 8, w2y + 120, g.COLOR_LIGHT_GRAY, f"Time: {t:.1f} s")

        for i in range(8):
            game.draw_printf(w2x + 8, w2y + 146 + i * 14, g.COLOR_GRAY, f"Line {i} - clipped at bottom")

        game.clear_clip()
        draw_window_border(game, w2x, w2y, w2w, w2h, "Text Clip", g.COLOR_WHITE)

        # === Window 3: Sprites ===
        game.set_clip(w3x, w3y, w3w, w3h)
        game.fill_rect(w3x, w3y, w3w, w3h, g.COLOR_RGB(20, 30, 20))

        for row in range(3):
            for col in range(10):
                sx = w3x - 20 + col * 68 + int(math.sin(t + col * 0.7) * 16)
                sy = w3y + 10 + row * 64 + int(math.cos(t + row * 1.1) * 10)
                sz = 24 + row * 16
                game.draw_sprite_scaled(star, sx, sy, sz, sz)

        big_x = w3x + w3w - 40 + int(math.sin(t * 0.8) * 60)
        game.draw_sprite_scaled(star, big_x, w3y + w3h // 2 - 40, 80, 80)

        game.clear_clip()
        draw_window_border(game, w3x, w3y, w3w, w3h, "Sprite Clip", g.COLOR_WHITE)

        game.draw_text(20, 460, "ESC to quit | All draws are clipped to their window region", g.COLOR_DARK_GRAY)

        game.update()
        game.wait_frame(60)

    game.free_sprite(star)


if __name__ == "__main__":
    main()
