"""12_sprite_transform.py - Sprite Scaling & Rotation

Tab key to switch between two modes:
  Mode A: Sprite Scaling  - draw_sprite_scaled, draw_sprite_frame_scaled at various sizes
  Mode B: Sprite Rotation - draw_sprite_rotated, draw_sprite_frame_rotated with animation

Controls:
  Mode A: Wheel/Q/E change scale, A/D change frame, F flip, R reset
  Mode B: Wheel/Q/E change angular speed, A/D change frame, F flip, SPACE pause, R reset
  ESC: quit

Learn: draw_sprite_scaled, draw_sprite_frame_scaled, draw_sprite_rotated,
       draw_sprite_frame_rotated, set_sprite_color_key, SPRITE_COLORKEY
"""

import pyezgame as g


def wrap_angle(a):
    while a >= 360.0:
        a -= 360.0
    while a < 0.0:
        a += 360.0
    return a


def draw_panel(game, x, y, w, h, title) -> None:
    game.fill_rect(x, y, w, h, g.COLOR_RGB(28, 34, 50))
    game.draw_rect(x, y, w, h, g.COLOR_RGB(84, 94, 120))
    game.fill_rect(x + 1, y + 1, w - 2, 22, g.COLOR_RGB(38, 48, 72))
    game.draw_text(x + 8, y + 7, title, g.COLOR_WHITE)


def draw_checkerboard(game, x, y, w, h, cell) -> None:
    c0 = g.COLOR_RGB(48, 54, 70)
    c1 = g.COLOR_RGB(62, 70, 90)
    py_ = y
    while py_ < y + h:
        px = x
        while px < x + w:
            cw = min(cell, x + w - px)
            ch = min(cell, y + h - py_)
            color = c0 if (((px - x) // cell + (py_ - y) // cell) & 1) else c1
            game.fill_rect(px, py_, cw, ch, color)
            px += cell
        py_ += cell


def draw_crosshair(game, cx, cy, size, color) -> None:
    game.draw_line(cx - size, cy, cx + size, cy, color)
    game.draw_line(cx, cy - size, cx, cy + size, color)


def create_ship_sprite(game):
    """17x17 ship sprite (odd size for rotation center)."""
    sid = game.create_sprite(17, 17)
    if sid < 0:
        return -1

    for y in range(17):
        for x in range(17):
            game.set_sprite_pixel(sid, x, y, g.COLORKEY_DEFAULT)

    # Nose
    for y in range(1, 7):
        span = y - 1
        for x in range(8 - span, 9 + span):
            game.set_sprite_pixel(sid, x, y, g.COLOR_WHITE)
    # Body
    for y in range(6, 13):
        for x in range(6, 11):
            game.set_sprite_pixel(sid, x, y, g.COLOR_CYAN)
    # Wings
    for x in range(2, 6):
        game.set_sprite_pixel(sid, x, 9, g.COLOR_GRAY)
        game.set_sprite_pixel(sid, x, 10, g.COLOR_GRAY)
    for x in range(11, 15):
        game.set_sprite_pixel(sid, x, 9, g.COLOR_GRAY)
        game.set_sprite_pixel(sid, x, 10, g.COLOR_GRAY)
    # Tail
    for x in (6, 7, 9, 10):
        game.set_sprite_pixel(sid, x, 13, g.COLOR_DARK_GRAY)
    # Flame
    for x in (7, 8, 9):
        game.set_sprite_pixel(sid, x, 14, g.COLOR_ORANGE)
    for x in (7, 9):
        game.set_sprite_pixel(sid, x, 15, g.COLOR_YELLOW)
    game.set_sprite_pixel(sid, 8, 16, g.COLOR_YELLOW)

    game.set_sprite_color_key(sid, g.COLORKEY_DEFAULT)
    return sid


def create_pulse_sheet(game):
    """64x16 pulse sheet: 4 frames, each 16x16."""
    sid = game.create_sprite(64, 16)
    if sid < 0:
        return -1

    for y in range(16):
        for x in range(64):
            game.set_sprite_pixel(sid, x, y, g.COLORKEY_DEFAULT)

    colors = [g.COLOR_RED, g.COLOR_ORANGE, g.COLOR_YELLOW, g.COLOR_WHITE]
    radii = [2, 3, 4, 3]

    for f in range(4):
        cx = f * 16 + 8
        cy = 8
        r = radii[f]
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                ax = abs(dx)
                ay = abs(dy)
                if ax + ay <= r:
                    game.set_sprite_pixel(sid, cx + dx, cy + dy, colors[f])
        for ddx, ddy in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
            game.set_sprite_pixel(sid, cx + ddx, cy + ddy, g.COLOR_WHITE)

    game.set_sprite_color_key(sid, g.COLORKEY_DEFAULT)
    return sid


def main() -> None:
    game = g.GameLib()
    SW, SH = 860, 580
    game.open(SW, SH, "12 - Sprite Transform", True)

    ship = create_ship_sprite(game)
    pulse = create_pulse_sheet(game)

    frame = 0
    flip = False
    scale = 4
    angle_speed = 3
    angle = 0.0
    spinning = True
    mode_b = False

    while not game.is_closed():
        if game.is_key_pressed(g.KEY_ESCAPE):
            break
        if game.is_key_pressed(g.KEY_TAB):
            mode_b = not mode_b

        # Shared controls
        if game.is_key_pressed(g.KEY_A) or game.is_key_pressed(g.KEY_LEFT):
            frame = (frame + 3) % 4
        if game.is_key_pressed(g.KEY_D) or game.is_key_pressed(g.KEY_RIGHT):
            frame = (frame + 1) % 4
        if game.is_key_pressed(g.KEY_F):
            flip = not flip

        wheel = game.get_mouse_wheel_delta()
        flags = g.SPRITE_COLORKEY | (g.SPRITE_FLIP_H if flip else 0)
        flip_text = "On" if flip else "Off"

        if not mode_b:
            # --- Mode A: Scaling ---
            if wheel != 0:
                scale += wheel
            if game.is_key_pressed(g.KEY_Q):
                scale -= 1
            if game.is_key_pressed(g.KEY_E):
                scale += 1
            scale = g.clamp(scale, 1, 6)

            if game.is_key_pressed(g.KEY_R):
                scale, frame, flip = 4, 0, False

            game.clear(g.COLOR_RGB(18, 22, 36))
            game.fill_rect(0, 0, SW, 56, g.COLOR_RGB(10, 14, 24))
            game.draw_text(20, 8, "MODE A: SCALING", g.COLOR_CYAN)
            game.draw_text(20, 24, "Wheel/Q/E scale  A/D frame  F flip  R reset  TAB switch  ESC quit", g.COLOR_WHITE)
            game.draw_printf(20, 40, g.COLOR_LIGHT_GRAY, f"Scale: {scale}x   Frame: {frame}   Flip: {flip_text}")

            # Source panel
            draw_panel(game, 20, 66, 200, 494, "Source Sprites")
            game.draw_text(36, 98, "Ship (17x17)", g.COLOR_LIGHT_GRAY)
            draw_checkerboard(game, 36, 116, 168, 100, 8)
            game.draw_rect(36, 116, 168, 100, g.COLOR_RGB(98, 110, 138))
            game.draw_sprite_ex(ship, 36 + (168 - 17) // 2, 116 + (100 - 17) // 2, g.SPRITE_COLORKEY)

            game.draw_text(36, 236, "Pulse sheet (64x16)", g.COLOR_LIGHT_GRAY)
            draw_checkerboard(game, 36, 256, 168, 80, 8)
            game.draw_rect(36, 256, 168, 80, g.COLOR_RGB(98, 110, 138))
            game.draw_sprite_scaled(pulse, 52, 276, 128, 32, g.SPRITE_COLORKEY)
            game.draw_rect(52 + frame * 32, 276, 32, 32, g.COLOR_GOLD)
            game.draw_text(36, 346, "4 frames, each 16x16", g.COLOR_GRAY)

            # Scaling panel
            draw_panel(game, 240, 66, 600, 230, "DrawSpriteScaled")
            game.draw_text(256, 98, "Scaled ship", g.COLOR_LIGHT_GRAY)
            draw_checkerboard(game, 256, 116, 280, 160, 10)
            game.draw_rect(256, 116, 280, 160, g.COLOR_RGB(98, 110, 138))
            game.draw_sprite_scaled(
                ship,
                256 + (280 - 17 * scale) // 2,
                116 + (160 - 17 * scale) // 2,
                17 * scale,
                17 * scale,
                flags,
            )
            game.draw_printf(256, 282, g.COLOR_WHITE, f"17x17 -> {17 * scale}x{17 * scale}")

            game.draw_text(560, 98, "Wide stretch", g.COLOR_LIGHT_GRAY)
            draw_checkerboard(game, 560, 116, 120, 72, 10)
            game.draw_rect(560, 116, 120, 72, g.COLOR_RGB(98, 110, 138))
            game.draw_sprite_scaled(ship, 560 + (120 - 96) // 2, 116 + (72 - 48) // 2, 96, 48, flags)
            game.draw_text(560, 196, "96x48", g.COLOR_GRAY)

            game.draw_text(700, 98, "Tall stretch", g.COLOR_LIGHT_GRAY)
            draw_checkerboard(game, 700, 116, 120, 160, 10)
            game.draw_rect(700, 116, 120, 160, g.COLOR_RGB(98, 110, 138))
            game.draw_sprite_scaled(ship, 700 + (120 - 48) // 2, 116 + (160 - 120) // 2, 48, 120, flags)
            game.draw_text(700, 282, "48x120", g.COLOR_GRAY)

            # Frame scaling panel
            draw_panel(game, 240, 310, 600, 250, "DrawSpriteFrameScaled")
            game.draw_text(256, 342, "Sheet preview", g.COLOR_LIGHT_GRAY)
            draw_checkerboard(game, 256, 360, 180, 80, 8)
            game.draw_rect(256, 360, 180, 80, g.COLOR_RGB(98, 110, 138))
            game.draw_sprite_scaled(pulse, 264, 380, 160, 32, g.SPRITE_COLORKEY)
            game.draw_rect(264 + frame * 40, 380, 40, 32, g.COLOR_GOLD)
            game.draw_text(256, 448, "A/D changes highlight", g.COLOR_GRAY)

            game.draw_text(460, 342, "Current frame scaled", g.COLOR_LIGHT_GRAY)
            draw_checkerboard(game, 460, 360, 360, 180, 10)
            game.draw_rect(460, 360, 360, 180, g.COLOR_RGB(98, 110, 138))
            game.draw_sprite_frame_scaled(
                pulse,
                460 + (360 - 16 * scale) // 2,
                360 + (180 - 16 * scale) // 2,
                16,
                16,
                frame,
                16 * scale,
                16 * scale,
                flags,
            )
            game.draw_printf(460, 546, g.COLOR_WHITE, f"16x16 -> {16 * scale}x{16 * scale}")

        else:
            # --- Mode B: Rotation ---
            if wheel > 0:
                angle_speed += 1
            if wheel < 0:
                angle_speed -= 1
            if game.is_key_pressed(g.KEY_Q):
                angle_speed -= 1
            if game.is_key_pressed(g.KEY_E):
                angle_speed += 1
            angle_speed = g.clamp(angle_speed, -12, 12)
            if game.is_key_pressed(g.KEY_SPACE):
                spinning = not spinning
            if game.is_key_pressed(g.KEY_R):
                angle, angle_speed, frame, flip, spinning = 0.0, 3, 0, False, True

            if spinning:
                angle = wrap_angle(angle + angle_speed)

            spin_text = "Running" if spinning else "Paused"

            game.clear(g.COLOR_RGB(18, 22, 36))
            game.fill_rect(0, 0, SW, 56, g.COLOR_RGB(10, 14, 24))
            game.draw_text(20, 8, "MODE B: ROTATION", g.COLOR_CYAN)
            game.draw_text(
                20,
                24,
                "Wheel/Q/E speed  A/D frame  F flip  SPACE pause  R reset  TAB switch  ESC quit",
                g.COLOR_WHITE,
            )
            game.draw_printf(
                20,
                40,
                g.COLOR_LIGHT_GRAY,
                f"Angle: {angle:.1f}   Speed: {angle_speed}   Frame: {frame}   Flip: {flip_text}   {spin_text}",
            )

            # Source panel
            draw_panel(game, 20, 66, 200, 494, "Source Sprites")
            game.draw_text(36, 98, "Ship (17x17)", g.COLOR_LIGHT_GRAY)
            draw_checkerboard(game, 36, 116, 168, 100, 8)
            game.draw_rect(36, 116, 168, 100, g.COLOR_RGB(98, 110, 138))
            game.draw_sprite_ex(ship, 36 + (168 - 17) // 2, 116 + (100 - 17) // 2, g.SPRITE_COLORKEY)

            game.draw_text(36, 236, "Pulse sheet (64x16)", g.COLOR_LIGHT_GRAY)
            draw_checkerboard(game, 36, 256, 168, 80, 8)
            game.draw_rect(36, 256, 168, 80, g.COLOR_RGB(98, 110, 138))
            game.draw_sprite_scaled(pulse, 52, 276, 128, 32, g.SPRITE_COLORKEY)
            game.draw_rect(52 + frame * 32, 276, 32, 32, g.COLOR_GOLD)
            game.draw_text(36, 346, "4 frames, each 16x16", g.COLOR_GRAY)

            # Rotation panel
            draw_panel(game, 240, 66, 600, 230, "DrawSpriteRotated")
            draw_checkerboard(game, 256, 96, 200, 180, 10)
            game.draw_rect(256, 96, 200, 180, g.COLOR_RGB(98, 110, 138))
            draw_crosshair(game, 356, 186, 14, g.COLOR_RGB(120, 138, 168))
            game.draw_sprite_rotated(ship, 356, 186, angle, flags)
            game.draw_text(256, 282, "Animated", g.COLOR_LIGHT_GRAY)

            # Static angle examples
            static_angles = [
                (480, 96, "0 deg", 0.0),
                (580, 96, "45 deg", 45.0),
                (700, 96, "90 deg", 90.0),
                (530, 198, "135 deg", 135.0),
                (650, 198, "180 deg", 180.0),
            ]
            for sx, sy, label, a in static_angles:
                draw_checkerboard(game, sx, sy, 80, 80, 10)
                game.draw_rect(sx, sy, 80, 80, g.COLOR_RGB(98, 110, 138))
                draw_crosshair(game, sx + 40, sy + 40, 10, g.COLOR_RGB(120, 138, 168))
                game.draw_sprite_rotated(ship, sx + 40, sy + 40, a, flags)
                game.draw_text(sx, sy + 82, label, g.COLOR_GRAY)

            # Frame rotation panel
            draw_panel(game, 240, 310, 600, 250, "DrawSpriteFrameRotated")
            draw_checkerboard(game, 256, 340, 180, 160, 10)
            game.draw_rect(256, 340, 180, 160, g.COLOR_RGB(98, 110, 138))
            draw_crosshair(game, 346, 420, 12, g.COLOR_RGB(120, 138, 168))
            game.draw_sprite_frame_rotated(pulse, 346, 420, 16, 16, frame, angle, flags)
            game.draw_text(256, 506, "Current pulse", g.COLOR_LIGHT_GRAY)

            for i in range(4):
                bx = 460 + i * 100
                by = 340
                draw_checkerboard(game, bx, by, 80, 72, 10)
                game.draw_rect(bx, by, 80, 72, g.COLOR_RGB(98, 110, 138))
                draw_crosshair(game, bx + 40, by + 36, 10, g.COLOR_RGB(120, 138, 168))
                game.draw_sprite_frame_rotated(pulse, bx + 40, by + 36, 16, 16, i, angle + i * 30.0, flags)
                game.draw_printf(bx, by + 76, g.COLOR_GRAY, f"Frame {i}")

            hlx = 460 + frame * 100
            game.draw_rect(hlx, 340, 80, 72, g.COLOR_GOLD)

            game.draw_text(460, 448, "A/D changes selected frame", g.COLOR_LIGHT_GRAY)
            game.draw_text(460, 468, "Each frame offset by 30 degrees", g.COLOR_GRAY)

        game.update()
        game.wait_frame(60)

    game.free_sprite(ship)
    game.free_sprite(pulse)


if __name__ == "__main__":
    main()
