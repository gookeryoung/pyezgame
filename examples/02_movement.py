"""02_movement.py - Movement and Physics

Two modes (press TAB to switch):
  Mode A: Arrow keys move a box around the screen.
  Mode B: A bouncing ball with a fading trail.
Learn: is_key_down, fill_rect, fill_circle, draw_circle, draw_printf,
       get_fps, get_delta_time, float physics, wall collision
"""
import gameui as g


def main():
    game = g.GameLib()
    game.open(640, 480, "02 - Movement and Physics", True)

    # --- Mode A: Keyboard controlled box ---
    box_x, box_y = 310.0, 230.0
    box_size = 20
    box_speed = 200.0  # pixels per second

    # --- Mode B: Bouncing ball ---
    ball_x, ball_y = 320.0, 240.0
    ball_vx, ball_vy = 240.0, 180.0  # pixels per second
    ball_r = 20

    # Trail for bouncing ball
    trail_x: list[float] = []
    trail_y: list[float] = []

    show_ball = False  # False = mode A (box), True = mode B (ball)

    while not game.is_closed():
        if game.is_key_pressed(g.KEY_ESCAPE):
            break
        if game.is_key_pressed(g.KEY_TAB):
            show_ball = not show_ball

        dt = game.get_delta_time()
        if dt > 0.05:
            dt = 0.05  # prevent first-frame jump

        if not show_ball:
            # --- Mode A: Keyboard Control ---
            if game.is_key_down(g.KEY_LEFT):
                box_x -= box_speed * dt
            if game.is_key_down(g.KEY_RIGHT):
                box_x += box_speed * dt
            if game.is_key_down(g.KEY_UP):
                box_y -= box_speed * dt
            if game.is_key_down(g.KEY_DOWN):
                box_y += box_speed * dt

            # Keep inside window bounds
            box_x = max(0.0, min(box_x, game.get_width() - box_size))
            box_y = max(0.0, min(box_y, game.get_height() - box_size))
        else:
            # --- Mode B: Bouncing Ball ---
            ball_x += ball_vx * dt
            ball_y += ball_vy * dt

            if ball_x - ball_r < 0:
                ball_x = float(ball_r)
                ball_vx = -ball_vx
            if ball_x + ball_r > game.get_width():
                ball_x = float(game.get_width() - ball_r)
                ball_vx = -ball_vx
            if ball_y - ball_r < 0:
                ball_y = float(ball_r)
                ball_vy = -ball_vy
            if ball_y + ball_r > game.get_height():
                ball_y = float(game.get_height() - ball_r)
                ball_vy = -ball_vy

            # Record trail
            trail_x.append(ball_x)
            trail_y.append(ball_y)
            if len(trail_x) > 64:
                trail_x.pop(0)
                trail_y.pop(0)

        # --- Drawing ---
        game.clear(g.COLOR_BLACK)

        if not show_ball:
            # Mode A drawing
            game.fill_rect(int(box_x), int(box_y), box_size, box_size, g.COLOR_CYAN)
            game.draw_text(10, 10, "Mode A: Arrow keys to move", g.COLOR_WHITE)
            game.draw_printf(10, 25, g.COLOR_GRAY, f"Position: {box_x:.0f}, {box_y:.0f}")
        else:
            # Mode B drawing: trail
            for i, (tx, ty) in enumerate(zip(trail_x, trail_y)):
                brightness = min(40 + i * 3, 255)
                c = g.COLOR_RGB(brightness, 0, 0)
                tr = 2 + i * ball_r // 64
                game.fill_circle(int(tx), int(ty), tr, c)
            # Ball
            game.fill_circle(int(ball_x), int(ball_y), ball_r, g.COLOR_RED)
            game.draw_circle(int(ball_x), int(ball_y), ball_r, g.COLOR_WHITE)
            game.draw_text(10, 10, "Mode B: Bouncing Ball", g.COLOR_WHITE)
            game.draw_printf(10, 25, g.COLOR_GRAY,
                             f"Ball: {ball_x:.0f}, {ball_y:.0f}  Speed: {ball_vx:.0f}, {ball_vy:.0f}")

        # Common HUD
        game.draw_printf(10, 460, g.COLOR_LIGHT_GRAY,
                         f"FPS: {game.get_fps():.0f}  |  TAB: Switch Mode  |  ESC: Quit")

        game.update()
        game.wait_frame(60)


if __name__ == "__main__":
    main()
