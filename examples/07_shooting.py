"""07_shooting.py - Simple Shooter

Control a ship to move left/right, press Space to shoot bullets at falling targets.
Learn: lists for multiple objects, bullet firing, collision destroy, is_key_pressed,
       load_sprite, draw_sprite_scaled, play_wav
"""

import os

import pyezgame as g

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

MAX_BULLETS = 30
MAX_ENEMIES = 15


def choose_existing_path(path_a, path_b):
    if os.path.isfile(path_a):
        return path_a
    if os.path.isfile(path_b):
        return path_b
    abs_a = os.path.join(SCRIPT_DIR, path_a)
    abs_b = os.path.join(SCRIPT_DIR, path_b)
    if os.path.isfile(abs_a):
        return abs_a
    if os.path.isfile(abs_b):
        return abs_b
    return path_a


class Bullet:
    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.active = False


class Enemy:
    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.speed = 0
        self.active = False


class Explosion:
    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.timer = 0
        self.active = False


def main() -> None:
    game = g.GameLib()
    game.open(640, 480, "07 - Shooting Stars", True)

    # Load sprite assets
    player_path = choose_existing_path(
        "../clib/assets/player_ship.png",
        "assets/player_ship.png",
    )
    enemy_path = choose_existing_path(
        "../clib/assets/enemy_ship.png",
        "assets/enemy_ship.png",
    )
    bullet_path = choose_existing_path("../clib/assets/bullet.png", "assets/bullet.png")
    explosion_path = choose_existing_path(
        "../clib/assets/explosion.png",
        "assets/explosion.png",
    )
    star_path = choose_existing_path("../clib/assets/star.png", "assets/star.png")

    spr_player = game.load_sprite(player_path)
    spr_enemy = game.load_sprite(enemy_path)
    spr_bullet = game.load_sprite(bullet_path)
    spr_explosion = game.load_sprite(explosion_path)
    spr_star = game.load_sprite(star_path)

    # Load sound assets
    shoot_sfx = choose_existing_path(
        "../clib/assets/sound/click.wav",
        "assets/sound/click.wav",
    )
    hit_sfx = choose_existing_path("../clib/assets/sound/hit.wav", "assets/sound/hit.wav")
    coin_sfx = choose_existing_path("../clib/assets/sound/coin.wav", "assets/sound/coin.wav")
    game_over_sfx = choose_existing_path(
        "../clib/assets/sound/game_over.wav",
        "assets/sound/game_over.wav",
    )

    # Player ship
    ship_x, ship_y = 300, 420
    ship_w, ship_h = 32, 32

    bullets = [Bullet() for _ in range(MAX_BULLETS)]
    enemies = [Enemy() for _ in range(MAX_ENEMIES)]
    explosions = [Explosion() for _ in range(MAX_ENEMIES)]

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
                        game.play_wav(shoot_sfx, 1, 600)
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
                        e.y = -24
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
                        game.play_wav(game_over_sfx, 1, 1000)

            # Collision: bullet vs enemy
            for b in bullets:
                if not b.active:
                    continue
                for e in enemies:
                    if not e.active:
                        continue
                    if g.GameLib.rect_overlap(b.x - 2, b.y - 4, 4, 8, e.x, e.y, 24, 24):
                        b.active = False
                        e.active = False
                        score += 1
                        game.play_wav(coin_sfx, 1, 800)
                        # Spawn explosion
                        for ex in explosions:
                            if not ex.active:
                                ex.active = True
                                ex.x = e.x
                                ex.y = e.y
                                ex.timer = 15
                                break
                        break

            # Collision: enemy vs ship
            for e in enemies:
                if not e.active:
                    continue
                if g.GameLib.rect_overlap(
                    e.x,
                    e.y,
                    24,
                    24,
                    ship_x,
                    ship_y,
                    ship_w,
                    ship_h,
                ):
                    e.active = False
                    lives -= 1
                    game.play_wav(hit_sfx, 1, 800)
                    if lives <= 0:
                        game_over = True
                        game.play_wav(game_over_sfx, 1, 1000)
        else:
            if game.is_key_pressed(g.KEY_R):
                score = 0
                lives = 5
                game_over = False
                for b in bullets:
                    b.active = False
                for e in enemies:
                    e.active = False
                for ex in explosions:
                    ex.active = False

        # --- Drawing ---
        game.clear(g.COLOR_BLACK)

        # Starfield background (use star sprite if loaded)
        for i in range(60):
            sx = (i * 137 + 59) % game.get_width()
            sy = (i * 251 + 31) % game.get_height()
            if spr_star >= 0:
                game.draw_sprite_scaled(spr_star, sx, sy, 4, 4, g.SPRITE_COLORKEY)
            else:
                game.set_pixel(sx, sy, g.COLOR_WHITE)

        # Bullets
        for b in bullets:
            if b.active:
                if spr_bullet >= 0:
                    game.draw_sprite_scaled(
                        spr_bullet,
                        b.x - 3,
                        b.y - 8,
                        6,
                        16,
                        g.SPRITE_COLORKEY,
                    )
                else:
                    game.fill_rect(b.x - 1, b.y - 4, 3, 8, g.COLOR_YELLOW)

        # Enemies
        for e in enemies:
            if e.active:
                if spr_enemy >= 0:
                    game.draw_sprite_scaled(
                        spr_enemy,
                        e.x,
                        e.y,
                        24,
                        24,
                        g.SPRITE_COLORKEY,
                    )
                else:
                    game.fill_rect(e.x, e.y, 24, 24, g.COLOR_RED)
                    game.draw_rect(e.x, e.y, 24, 24, g.COLOR_ORANGE)

        # Explosions
        for ex in explosions:
            if ex.active:
                if spr_explosion >= 0:
                    game.draw_sprite_scaled(
                        spr_explosion,
                        ex.x - 4,
                        ex.y - 4,
                        32,
                        32,
                        g.SPRITE_COLORKEY,
                    )
                else:
                    game.fill_circle(ex.x + 12, ex.y + 12, 16, g.COLOR_ORANGE)
                ex.timer -= 1
                if ex.timer <= 0:
                    ex.active = False

        # Ship
        if spr_player >= 0:
            game.draw_sprite_scaled(
                spr_player,
                ship_x,
                ship_y,
                ship_w,
                ship_h,
                g.SPRITE_COLORKEY,
            )
        else:
            game.fill_triangle(
                ship_x + ship_w // 2,
                ship_y - 5,
                ship_x,
                ship_y + ship_h,
                ship_x + ship_w,
                ship_y + ship_h,
                g.COLOR_CYAN,
            )

        # HUD
        game.draw_printf(10, 10, g.COLOR_WHITE, f"Score: {score}")
        game.draw_printf(10, 25, g.COLOR_GREEN, f"Lives: {lives}")
        fps = game.get_fps()
        game.draw_printf(10, 40, g.COLOR_WHITE, f"FPS: {fps:.2f}")
        game.draw_text(game.get_width() - 230, 10, "Left/Right + Space", g.COLOR_GRAY)

        if game_over:
            game.fill_rect(170, 180, 300, 100, g.COLOR_DARK_GRAY)
            game.draw_rect(170, 180, 300, 100, g.COLOR_WHITE)
            game.draw_text_scale(210, 200, "GAME OVER", g.COLOR_RED, 16, 16)
            game.draw_printf(240, 240, g.COLOR_WHITE, f"Final Score: {score}")
            game.draw_text(220, 260, "Press R to restart", g.COLOR_YELLOW)

        game.update()
        game.wait_frame(60)

    # Free sprites
    for s in [spr_player, spr_enemy, spr_bullet, spr_explosion, spr_star]:
        if s >= 0:
            game.free_sprite(s)


if __name__ == "__main__":
    main()
