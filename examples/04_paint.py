"""04_paint.py - Simple Paint

A simple paint program: draw with mouse, change color/brush/clear with keyboard.
Learn: get_mouse_x/y, is_mouse_down, is_mouse_released, get_mouse_wheel_delta, is_active
"""
import gameui as g


def main():
    game = g.GameLib()
    game.open(640, 480, "04 - Paint", True, True)

    palette = [
        g.COLOR_WHITE, g.COLOR_RED, g.COLOR_GREEN, g.COLOR_BLUE,
        g.COLOR_YELLOW, g.COLOR_CYAN, g.COLOR_ORANGE, g.COLOR_PINK,
    ]
    color_index = 0
    brush_size = 4

    # Draw background once (don't clear each frame, so drawings stay)
    game.clear(g.COLOR_BLACK)

    while not game.is_closed():
        mx = game.get_mouse_x()
        my = game.get_mouse_y()
        wheel_steps = game.get_mouse_wheel_delta() // 120

        # Switch color: 1-8 number keys
        key_map = [g.KEY_1, g.KEY_2, g.KEY_3, g.KEY_4,
                   g.KEY_5, g.KEY_6, g.KEY_7, g.KEY_8]
        for i, key in enumerate(key_map):
            if game.is_key_pressed(key):
                color_index = i

        # Brush size: Up/Down or mouse wheel
        if game.is_key_pressed(g.KEY_UP) and brush_size < 30:
            brush_size += 2
        if game.is_key_pressed(g.KEY_DOWN) and brush_size > 1:
            brush_size -= 2
        if wheel_steps != 0:
            brush_size += wheel_steps * 2
            brush_size = max(1, min(30, brush_size))

        # Clear screen: C key
        if game.is_key_pressed(g.KEY_C):
            game.clear(g.COLOR_BLACK)

        # Click palette on release, avoid selecting colors while dragging.
        if game.is_mouse_released(g.MOUSE_LEFT) and 4 <= my < 22:
            for i in range(len(palette)):
                bx = 10 + i * 22
                if bx <= mx < bx + 18:
                    color_index = i
                    break

        # Left button: draw
        if game.is_mouse_down(g.MOUSE_LEFT) and my > 30 and game.is_active():
            game.fill_circle(mx, my, brush_size, palette[color_index])

        # Right button: eraser
        if game.is_mouse_down(g.MOUSE_RIGHT) and my > 30 and game.is_active():
            game.fill_circle(mx, my, brush_size + 4, g.COLOR_BLACK)

        # Top toolbar (redraw each frame)
        game.fill_rect(0, 0, game.get_width(), 28, g.COLOR_DARK_GRAY)

        # Color palette
        for i in range(len(palette)):
            bx = 10 + i * 22
            game.fill_rect(bx, 4, 18, 18, palette[i])
            if i == color_index:
                game.draw_rect(bx - 1, 3, 20, 20, g.COLOR_WHITE)

        # Brush preview
        game.fill_circle(210, 13, brush_size, palette[color_index])

        # Hints
        game.draw_text(240, 4, "1-8/Click:Color  Up/Down/Wheel:Size", g.COLOR_LIGHT_GRAY)
        game.draw_text(240, 16, "L:Draw  R:Erase  C:Clear", g.COLOR_LIGHT_GRAY)
        active_text = "ACTIVE" if game.is_active() else "PAUSED"
        active_color = g.COLOR_GREEN if game.is_active() else g.COLOR_YELLOW
        game.draw_text(520, 16, active_text, active_color)

        game.update()
        game.wait_frame(60)


if __name__ == "__main__":
    main()
