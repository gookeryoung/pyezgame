"""07_shooting.py - Simple Shooter

Control a ship to move left/right, press Space to shoot bullets at falling targets.
Learn: lists for multiple objects, bullet firing, collision destroy, is_key_pressed
"""
import gameui as g

MAX_BULLETS = 30
MAX_ENEMIES = 15


class Bullet:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.active = False


class Enemy:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = 0
        self.active = False


def main():
    game = g.GameLib()
    game.open(640, 480, "07 - Shooting Stars", True)

    # Player ship
    ship_x, ship_y = 300, 440
    ship_w, ship_h = 30, 20

    bullets = [Bullet() for _ in range(MAX_BULLETS)]
    enemies = [Enemy() for _ in range(MAX_ENEMIES)]

    score = 0
    spawn_timer = 0
    lives = 5
    game_over = False

    while not game.is_closed():
        if game.is_key_pressed(g.KEY_ESCAPE):
            break

        if not game_over:
            # Ship movement
            if game.is_key_down(g.KEY_LEFT):
                ship_x -= 5
            if game.is_key_down(g.KEY_RIGHT):
                ship_x += 5
            ship_x = max(0, min(ship_x, game.get_width() - ship_w))

            # Fire bullet
            if game.is_key_pressed(g.KEY_SPACE):
                for b in bullets:
                    if not b.active:
                        b.active = True
                        b.x = ship_x + ship_w // 2
                        b.y = ship_y - 5
                        break

            # Update bullets
            for b in bullets:
                if not b.active:
                    continue
                b.y -= 8
                if b.y < 0:
                    b.active = False

            # Spawn enemy
            spawn_timer += 1
            rate = max(12, 40 - score // 3)
            if spawn_timer >= rate:
                spawn_timer = 0
                for e in enemies:
                    if not e.active:
                        e.active = True
                        e.x = g.GameLib.random(10, game.get_width() - 30)
                        e.y = -20
                        e.speed = g.GameLib.random(1, 3 + score // 15)
                        break

            # Update enemies
            for e in enemies:
                if not e.active:
                    continue
                e.y += e.speed
                if e.y > game.get_height():
                    e.active = False
                    lives -= 1
                    if lives <= 0:
                        game_over = True

            # Collision: bullet vs enemy
            for b in bullets:
                if not b.active:
                    continue
                for e in enemies:
                    if not e.active:
                        continue
                    if g.GameLib.rect_overlap(b.x - 2, b.y - 4, 4, 8,
                                              e.x, e.y, 20, 20):
                        b.active = False
                        e.active = False
                        score += 1
                        break

            # Collision: enemy vs ship
            for e in enemies:
                if not e.active:
                    continue
                if g.GameLib.rect_overlap(e.x, e.y, 20, 20,
                                          ship_x, ship_y, ship_w, ship_h):
                    e.active = False
                    lives -= 1
                    if lives <= 0:
                        game_over = True
        else:
            if game.is_key_pressed(g.KEY_R):
                score = 0
                lives = 5
                game_over = False
                for b in bullets:
                    b.active = False
                for e in enemies:
                    e.active = False

        # --- Drawing ---
        game.clear(g.COLOR_BLACK)

        # Starfield background
        for i in range(60):
            sx = (i * 137 + 59) % game.get_width()
            sy = (i * 251 + 31) % game.get_height()
            game.set_pixel(sx, sy, g.COLOR_WHITE)

        # Bullets
        for b in bullets:
            if b.active:
                game.fill_rect(b.x - 1, b.y - 4, 3, 8, g.COLOR_YELLOW)

        # Enemies (red squares)
        for e in enemies:
            if e.active:
                game.fill_rect(e.x, e.y, 20, 20, g.COLOR_RED)
                game.draw_rect(e.x, e.y, 20, 20, g.COLOR_ORANGE)

        # Ship (triangle)
        game.fill_triangle(
            ship_x + ship_w // 2, ship_y - 5,
            ship_x, ship_y + ship_h,
            ship_x + ship_w, ship_y + ship_h,
            g.COLOR_CYAN)

        # HUD
        game.draw_printf(10, 10, g.COLOR_WHITE, f"Score: {score}")
        game.draw_printf(10, 25, g.COLOR_GREEN, f"Lives: {lives}")
        game.draw_text(game.get_width() - 230, 10, "Left/Right + Space", g.COLOR_GRAY)

        if game_over:
            game.fill_rect(170, 180, 300, 100, g.COLOR_DARK_GRAY)
            game.draw_rect(170, 180, 300, 100, g.COLOR_WHITE)
            game.draw_text_scale(210, 200, "GAME OVER", g.COLOR_RED, 16, 16)
            game.draw_printf(240, 240, g.COLOR_WHITE, f"Final Score: {score}")
            game.draw_text(220, 260, "Press R to restart", g.COLOR_YELLOW)

        game.update()
        game.wait_frame(60)


if __name__ == "__main__":
    main()
