"""05_sprites.py - Sprites & Animation

Tab key to switch between two modes:
  Mode A: Sprite basics - create sprite with code, draw, flip, scale, frame extraction
  Mode B: Sprite animation - character walks with direction-based frame animation
Learn: create_sprite, set_sprite_pixel, draw_sprite, draw_sprite_ex, draw_sprite_scaled,
       draw_sprite_frame_scaled, free_sprite, get_delta_time
"""
import pyezgame as g


def create_ship_sprite(game):
    """16x16 small ship sprite, drawn with code."""
    sid = game.create_sprite(16, 16)
    if sid < 0:
        return -1

    for y in range(16):
        for x in range(16):
            game.set_sprite_pixel(sid, x, y, 0x00000000)

    # Body (cyan)
    for y in range(4, 14):
        for x in range(6, 10):
            game.set_sprite_pixel(sid, x, y, g.COLOR_CYAN)

    # Nose (white)
    for dy in range(2, 4):
        for dx in range(7, 9):
            game.set_sprite_pixel(sid, dx, dy, g.COLOR_WHITE)

    # Left wing
    for x in range(1, 6):
        game.set_sprite_pixel(sid, x, 9, g.COLOR_GRAY)
        game.set_sprite_pixel(sid, x, 10, g.COLOR_GRAY)
    # Right wing
    for x in range(10, 15):
        game.set_sprite_pixel(sid, x, 9, g.COLOR_GRAY)
        game.set_sprite_pixel(sid, x, 10, g.COLOR_GRAY)

    # Tail
    game.set_sprite_pixel(sid, 5, 13, g.COLOR_DARK_GRAY)
    game.set_sprite_pixel(sid, 10, 13, g.COLOR_DARK_GRAY)

    # Engine flame
    game.set_sprite_pixel(sid, 7, 14, g.COLOR_ORANGE)
    game.set_sprite_pixel(sid, 8, 14, g.COLOR_ORANGE)
    game.set_sprite_pixel(sid, 7, 15, g.COLOR_YELLOW)
    game.set_sprite_pixel(sid, 8, 15, g.COLOR_YELLOW)

    return sid


def create_anim_sheet(game):
    """32x8 sprite sheet, 4 frames each 8x8 (pulsing circle animation)."""
    sid = game.create_sprite(32, 8)
    if sid < 0:
        return -1

    for y in range(8):
        for x in range(32):
            game.set_sprite_pixel(sid, x, y, 0x00000000)

    colors = [g.COLOR_RED, g.COLOR_ORANGE, g.COLOR_YELLOW, g.COLOR_WHITE]
    sizes = [1, 2, 3, 2]
    for f in range(4):
        cx = f * 8 + 4
        cy = 4
        s = sizes[f]
        for dy in range(-s, s + 1):
            for dx in range(-s, s + 1):
                if dx * dx + dy * dy <= s * s:
                    game.set_sprite_pixel(sid, cx + dx, cy + dy, colors[f])
    return sid


def create_char_sheet(game):
    """36x64 character sprite sheet: 4 directions x 3 frames, each 12x16."""
    fw, fh = 12, 16
    cols, rows = 3, 4
    sid = game.create_sprite(fw * cols, fh * rows)
    if sid < 0:
        return -1

    for y in range(fh * rows):
        for x in range(fw * cols):
            game.set_sprite_pixel(sid, x, y, 0x00000000)

    skin = g.COLOR_RGB(255, 200, 150)
    hair = g.COLOR_BROWN
    shirt = g.COLOR_BLUE
    pants = g.COLOR_DARK_BLUE
    shoe = g.COLOR_DARK_GRAY

    for d in range(4):
        for f in range(3):
            ox = f * fw
            oy = d * fh

            # Head (4x4)
            for dy in range(4):
                for dx in range(4):
                    game.set_sprite_pixel(sid, ox + 4 + dx, oy + dy, skin)
            # Hair
            for dx in range(4):
                game.set_sprite_pixel(sid, ox + 4 + dx, oy, hair)
            # Body (6x5)
            for dy in range(4, 9):
                for dx in range(6):
                    game.set_sprite_pixel(sid, ox + 3 + dx, oy + dy, shirt)
            # Pants (6x3)
            for dy in range(9, 12):
                for dx in range(6):
                    game.set_sprite_pixel(sid, ox + 3 + dx, oy + dy, pants)
            # Feet
            if f == 0:
                left_foot_x, right_foot_x = 3, 7
            elif f == 1:
                left_foot_x, right_foot_x = 2, 8
            else:
                left_foot_x, right_foot_x = 4, 6
            for dy in range(12, 14):
                for fx in (left_foot_x, right_foot_x):
                    game.set_sprite_pixel(sid, ox + fx, oy + dy, shoe)
                    game.set_sprite_pixel(sid, ox + fx + 1, oy + dy, shoe)
            # Eyes
            if d == 0:
                game.set_sprite_pixel(sid, ox + 5, oy + 2, g.COLOR_BLACK)
                game.set_sprite_pixel(sid, ox + 7, oy + 2, g.COLOR_BLACK)
            elif d == 1:
                game.set_sprite_pixel(sid, ox + 4, oy + 2, g.COLOR_BLACK)
            elif d == 2:
                game.set_sprite_pixel(sid, ox + 7, oy + 2, g.COLOR_BLACK)
            else:
                for dx in range(4):
                    game.set_sprite_pixel(sid, ox + 4 + dx, oy + 1, hair)
    return sid


def main() -> None:
    game = g.GameLib()
    game.open(640, 480, "05 - Sprites & Animation", True)

    ship = create_ship_sprite(game)
    anim_sheet = create_anim_sheet(game)
    char_sheet = create_char_sheet(game)

    # Mode A state
    ship_x, ship_y = 300, 350
    anim_frame, anim_timer = 0, 0

    # Mode B state
    fw, fh, char_scale = 12, 16, 3
    px, py = 300.0, 220.0
    char_speed = 100.0
    char_dir, char_frame = 0, 0
    char_anim_timer = 0.0
    char_moving = False

    mode_b = False

    while not game.is_closed():
        if game.is_key_pressed(g.KEY_ESCAPE):
            break
        if game.is_key_pressed(g.KEY_TAB):
            mode_b = not mode_b

        dt = game.get_delta_time()

        if not mode_b:
            # --- Mode A: Sprite Basics ---
            if game.is_key_down(g.KEY_LEFT):
                ship_x -= 3
            if game.is_key_down(g.KEY_RIGHT):
                ship_x += 3
            if game.is_key_down(g.KEY_UP):
                ship_y -= 3
            if game.is_key_down(g.KEY_DOWN):
                ship_y += 3

            anim_timer += 1
            if anim_timer >= 10:
                anim_timer = 0
                anim_frame = (anim_frame + 1) % 4

            game.clear(g.COLOR_BLACK)

            game.draw_text(20, 20, "DrawSprite (normal):", g.COLOR_WHITE)
            game.draw_sprite(ship, 20, 40)

            game.draw_text(20, 70, "DrawSpriteEx (flipped):", g.COLOR_WHITE)
            game.draw_sprite_ex(ship, 20, 90, g.SPRITE_FLIP_H)
            game.draw_text(50, 95, "H", g.COLOR_GRAY)
            game.draw_sprite_ex(ship, 80, 90, g.SPRITE_FLIP_V)
            game.draw_text(110, 95, "V", g.COLOR_GRAY)
            game.draw_sprite_ex(ship, 140, 90, g.SPRITE_FLIP_H | g.SPRITE_FLIP_V)
            game.draw_text(170, 95, "H+V", g.COLOR_GRAY)

            game.draw_text(20, 130, "DrawSpriteFrameScaled (sprite sheet):", g.COLOR_WHITE)
            game.draw_sprite_scaled(anim_sheet, 20, 150, 64, 16)
            game.draw_rect(20, 150, 64, 16, g.COLOR_GRAY)
            game.draw_text(100, 148, "<-- full sheet", g.COLOR_GRAY)
            game.draw_text(20, 172, "Current frame:", g.COLOR_GRAY)
            game.draw_sprite_frame_scaled(anim_sheet, 130, 162, 8, 8, anim_frame, 32, 32)
            game.draw_sprite_frame_scaled(anim_sheet, 170, 162, 8, 8, anim_frame, 32, 32, g.SPRITE_FLIP_H)

            game.draw_text(20, 200, "Move with arrow keys:", g.COLOR_WHITE)
            game.draw_sprite(ship, ship_x, ship_y)

            game.draw_text(400, 20, "DrawSpriteScaled (4x):", g.COLOR_WHITE)
            game.draw_sprite_scaled(ship, 400, 40, 64, 64)
            game.draw_rect(400, 40, 64, 64, g.COLOR_GRAY)

            game.draw_text(10, 460, "[TAB] Switch to Animation mode | Arrows: move ship", g.COLOR_DARK_GRAY)

        else:
            # --- Mode B: Sprite Animation ---
            char_moving = False
            if game.is_key_down(g.KEY_DOWN) or game.is_key_down(g.KEY_S):
                py += char_speed * dt
                char_dir = 0
                char_moving = True
            if game.is_key_down(g.KEY_LEFT) or game.is_key_down(g.KEY_A):
                px -= char_speed * dt
                char_dir = 1
                char_moving = True
            if game.is_key_down(g.KEY_RIGHT) or game.is_key_down(g.KEY_D):
                px += char_speed * dt
                char_dir = 2
                char_moving = True
            if game.is_key_down(g.KEY_UP) or game.is_key_down(g.KEY_W):
                py -= char_speed * dt
                char_dir = 3
                char_moving = True

            px = max(0.0, min(px, game.get_width() - fw * char_scale))
            py = max(0.0, min(py, game.get_height() - fh * char_scale))

            if char_moving:
                char_anim_timer += dt
                if char_anim_timer >= 0.15:
                    char_anim_timer = 0.0
                    char_frame = (char_frame + 1) % 3
            else:
                char_frame = 0
                char_anim_timer = 0.0

            game.clear(g.COLOR_DARK_GREEN)

            # Ground decoration
            for i in range(30):
                gx = (i * 97 + 13) % game.get_width()
                gy = (i * 173 + 47) % game.get_height()
                game.fill_rect(gx, gy, 3, 3, g.COLOR_GREEN)

            # Character
            frame_index = char_dir * 3 + char_frame
            game.draw_sprite_frame_scaled(char_sheet, int(px), int(py),
                                          fw, fh, frame_index,
                                          fw * char_scale, fh * char_scale)

            # Sheet preview (top right)
            game.draw_text(470, 10, "Sprite Sheet:", g.COLOR_WHITE)
            pv_scale = 2
            pv_x, pv_y = 470, 25
            game.draw_sprite_scaled(char_sheet, pv_x, pv_y, fw * 3 * pv_scale, fh * 4 * pv_scale)
            game.draw_rect(pv_x, pv_y, fw * 3 * pv_scale, fh * 4 * pv_scale, g.COLOR_GRAY)
            game.draw_rect(pv_x + char_frame * fw * pv_scale, pv_y + char_dir * fh * pv_scale,
                           fw * pv_scale, fh * pv_scale, g.COLOR_YELLOW)

            dir_names = ["Down", "Left", "Right", "Up"]
            game.draw_text(10, 10, "WASD / Arrow keys to move", g.COLOR_WHITE)
            game.draw_printf(10, 25, g.COLOR_GRAY, f"Dir: {dir_names[char_dir]}  Frame: {char_frame}")
            game.draw_text(10, 460, "[TAB] Switch to Sprite Basics mode", g.COLOR_DARK_GRAY)

        game.update()
        game.wait_frame(60)

    game.free_sprite(ship)
    game.free_sprite(anim_sheet)
    game.free_sprite(char_sheet)


if __name__ == "__main__":
    main()
