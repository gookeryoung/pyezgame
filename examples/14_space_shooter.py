"""14_space_shooter.py - Space Shooter

The most comprehensive example: a space shooting game.
Features: asset-based player/bullets/explosions, scrolling starfield background,
          enemy formations, bullet system, collision detection, sound effects,
          scoring, difficulty scaling.
Learn: comprehensive use of all core GameLib APIs
"""

from __future__ import annotations

import pyezgame as g

W, H = 480, 640
MAX_STARS = 80
MAX_BULLETS = 30
MAX_ENEMIES = 20
MAX_EXPLOSIONS = 15
MAX_ENEMY_BULLETS = 20


class Star:
    def __init__(self, x: float, y: float, speed: float, color: int) -> None:
        self.x, self.y, self.speed, self.color = float(x), float(y), float(speed), int(color)


class Bullet:
    def __init__(self) -> None:
        self.x, self.y = 0.0, 0.0
        self.active = False


class Enemy:
    def __init__(self) -> None:
        self.x, self.y, self.vx, self.vy = 0.0, 0.0, 0.0, 0.0
        self.hp = 0
        self.active = False
        self.type = 0


class Explosion:
    def __init__(self) -> None:
        self.x, self.y = 0.0, 0.0
        self.timer = 0
        self.active = False


class EnemyBullet:
    def __init__(self) -> None:
        self.x, self.y, self.vy = 0.0, 0.0, 0.0
        self.active = False


def spawn_explosion(explosions: list[Explosion], x: float, y: float, timer: int) -> None:
    for e in explosions:
        if not e.active:
            e.active = True
            e.x, e.y, e.timer = x, y, timer
            return


def create_player_sprite(game: g.GameLib) -> int:
    sid = game.create_sprite(24, 24)
    if sid < 0:
        return -1
    for y in range(24):
        for x in range(24):
            game.set_sprite_pixel(sid, x, y, 0)
    for y in range(4, 20):
        for x in range(9, 15):
            game.set_sprite_pixel(sid, x, y, g.COLOR_CYAN)
    for x in range(10, 14):
        game.set_sprite_pixel(sid, x, 2, g.COLOR_WHITE)
        game.set_sprite_pixel(sid, x, 3, g.COLOR_WHITE)
    for x in (11, 12):
        game.set_sprite_pixel(sid, x, 0, g.COLOR_WHITE)
        game.set_sprite_pixel(sid, x, 1, g.COLOR_WHITE)
    for x in range(2, 9):
        for y in range(13, 17):
            game.set_sprite_pixel(sid, x, y, g.COLOR_GRAY)
    for x in range(15, 22):
        for y in range(13, 17):
            game.set_sprite_pixel(sid, x, y, g.COLOR_GRAY)
    game.set_sprite_pixel(sid, 11, 20, g.COLOR_ORANGE)
    game.set_sprite_pixel(sid, 12, 20, g.COLOR_ORANGE)
    game.set_sprite_pixel(sid, 11, 21, g.COLOR_YELLOW)
    game.set_sprite_pixel(sid, 12, 21, g.COLOR_YELLOW)
    return sid


def create_enemy_sprite(game: g.GameLib, body_color: int) -> int:
    sid = game.create_sprite(20, 20)
    if sid < 0:
        return -1
    for y in range(20):
        for x in range(20):
            game.set_sprite_pixel(sid, x, y, 0)
    for y in range(2, 14):
        half = 14 - y
        cx = 10
        for x in range(max(0, cx - half), min(20, cx + half)):
            game.set_sprite_pixel(sid, x, y, body_color)
    for y in range(3, 8):
        game.set_sprite_pixel(sid, 1, y, g.COLOR_DARK_GRAY)
        game.set_sprite_pixel(sid, 18, y, g.COLOR_DARK_GRAY)
    for dx, dy in [(9, 5), (10, 5), (9, 6), (10, 6)]:
        game.set_sprite_pixel(sid, dx, dy, g.COLOR_YELLOW)
    return sid


def main() -> None:
    game = g.GameLib()
    game.open(W, H, "14 - Space Shooter", True)

    player_path = g.get_asset_path("plane0.png")
    bullet_path = g.get_asset_path("bullet.png")
    explosion_path = g.get_asset_path("explosion.png")

    shoot_sfx = g.get_asset_path("sound/click.wav")
    enemy_hit_sfx = g.get_asset_path("sound/hit.wav")
    enemy_down_sfx = g.get_asset_path("sound/coin.wav")
    level_up_sfx = g.get_asset_path("sound/note_do_high.wav")
    player_hit_sfx = g.get_asset_path("sound/explosion.wav")
    game_over_sfx = g.get_asset_path("sound/game_over.wav")
    restart_sfx = g.get_asset_path("sound/click.wav")

    spr_player = game.load_sprite(player_path)
    if spr_player >= 0:
        game.set_sprite_color_key(spr_player, g.COLORKEY_DEFAULT)
    else:
        spr_player = create_player_sprite(game)
        if spr_player >= 0:
            game.set_sprite_color_key(spr_player, 0)

    spr_bullet = game.load_sprite(bullet_path)
    if spr_bullet >= 0:
        game.set_sprite_color_key(spr_bullet, g.COLORKEY_DEFAULT)

    spr_explosion = game.load_sprite(explosion_path)
    if spr_explosion >= 0:
        game.set_sprite_color_key(spr_explosion, g.COLORKEY_DEFAULT)

    spr_enemy1 = create_enemy_sprite(game, g.COLOR_RED)
    spr_enemy2 = create_enemy_sprite(game, g.COLOR_MAGENTA)
    if spr_enemy1 >= 0:
        game.set_sprite_color_key(spr_enemy1, 0)
    if spr_enemy2 >= 0:
        game.set_sprite_color_key(spr_enemy2, 0)

    player_w = game.get_sprite_width(spr_player) if spr_player >= 0 else 24
    player_h = game.get_sprite_height(spr_player) if spr_player >= 0 else 24
    enemy_w, enemy_h = 20, 20
    player_bullet_w, player_bullet_h = 10, 20
    enemy_bullet_w, enemy_bullet_h = 8, 18
    explosion_life = 16

    stars = []
    for _ in range(MAX_STARS):
        spd = g.GameLib.random(1, 4)
        b = min(80 + int(spd * 40), 255)
        stars.append(
            Star(
                float(g.GameLib.random(0, W - 1)),
                float(g.GameLib.random(0, H - 1)),
                float(spd),
                g.COLOR_RGB(b, b, b),
            ),
        )

    px = W / 2.0 - player_w / 2.0
    py = H - player_h - 28.0

    bullets = [Bullet() for _ in range(MAX_BULLETS)]
    enemies = [Enemy() for _ in range(MAX_ENEMIES)]
    e_bullets = [EnemyBullet() for _ in range(MAX_ENEMY_BULLETS)]
    explosions = [Explosion() for _ in range(MAX_EXPLOSIONS)]

    score, lives, level, kill_count = 0, 3, 1, 0
    game_over = False
    invincible = 0
    shoot_timer = 0
    shoot_sfx_cooldown = 0
    spawn_timer = 0

    while not game.is_closed():
        sfx_to_play = None
        sfx_priority = 0
        if game.is_key_pressed(g.KEY_ESCAPE):
            break

        def queue_sound(candidate: str, priority: int) -> None:
            nonlocal sfx_to_play, sfx_priority
            if candidate and priority >= sfx_priority:
                sfx_to_play = candidate
                sfx_priority = priority

        if not game_over:
            if shoot_sfx_cooldown > 0:
                shoot_sfx_cooldown -= 1

            spd = 5.0
            if game.is_key_down(g.KEY_LEFT):
                px -= spd
            if game.is_key_down(g.KEY_RIGHT):
                px += spd
            if game.is_key_down(g.KEY_UP):
                py -= spd
            if game.is_key_down(g.KEY_DOWN):
                py += spd
            px = max(0.0, min(px, W - player_w))
            py = max(0.0, min(py, H - player_h))

            if game.is_key_down(g.KEY_SPACE):
                shoot_timer += 1
                if shoot_timer >= 6:
                    shoot_timer = 0
                    for b in bullets:
                        if not b.active:
                            b.active = True
                            b.x = px + player_w / 2.0 - player_bullet_w / 2.0
                            b.y = py - player_bullet_h + 6
                            if shoot_sfx_cooldown <= 0:
                                queue_sound(shoot_sfx, 1)
                                shoot_sfx_cooldown = 10
                            break
            else:
                shoot_timer = 5

            for b in bullets:
                if b.active:
                    b.y -= 10
                    if b.y < -player_bullet_h:
                        b.active = False

            spawn_timer += 1
            rate = max(15, 50 - level * 5)
            if spawn_timer >= rate:
                spawn_timer = 0
                for e in enemies:
                    if not e.active:
                        e.active = True
                        e.x = float(g.GameLib.random(10, W - 30))
                        e.y = float(g.GameLib.random(-80, -20))
                        e.vx = float(g.GameLib.random(-2, 2))
                        e.vy = float(g.GameLib.random(1, 2 + level // 2))
                        e.type = g.GameLib.random(0, 1)
                        e.hp = 1 if e.type == 0 else 2
                        break

            for e in enemies:
                if not e.active:
                    continue
                e.x += e.vx
                e.y += e.vy
                if e.x < 0 or e.x > W - enemy_w:
                    e.vx = -e.vx
                if e.y > H + enemy_h:
                    e.active = False
                if g.GameLib.random(0, 200) < 1 + level:
                    for eb in e_bullets:
                        if not eb.active:
                            eb.active = True
                            eb.x = e.x + enemy_w / 2.0 - enemy_bullet_w / 2.0
                            eb.y = e.y + enemy_h - 4
                            eb.vy = 4.0 + level * 0.5
                            break

            for eb in e_bullets:
                if eb.active:
                    eb.y += eb.vy
                    if eb.y > H + enemy_bullet_h:
                        eb.active = False

            for b in bullets:
                if not b.active:
                    continue
                for e in enemies:
                    if not e.active:
                        continue
                    if g.GameLib.rect_overlap(
                        int(b.x),
                        int(b.y),
                        player_bullet_w,
                        player_bullet_h,
                        int(e.x),
                        int(e.y),
                        enemy_w,
                        enemy_h,
                    ):
                        b.active = False
                        e.hp -= 1
                        if e.hp <= 0:
                            e.active = False
                            score += (e.type + 1) * 100
                            kill_count += 1
                            queue_sound(enemy_down_sfx, 3)
                            if kill_count >= 10 + level * 5:
                                level += 1
                                kill_count = 0
                                queue_sound(level_up_sfx, 4)
                            spawn_explosion(explosions, e.x + enemy_w / 2.0, e.y + enemy_h / 2.0, explosion_life)
                        else:
                            queue_sound(enemy_hit_sfx, 2)
                        break

            if invincible > 0:
                invincible -= 1
            else:
                for eb in e_bullets:
                    if not eb.active:
                        continue
                    if g.GameLib.rect_overlap(
                        int(eb.x),
                        int(eb.y),
                        enemy_bullet_w,
                        enemy_bullet_h,
                        int(px) + 6,
                        int(py) + 6,
                        player_w - 12,
                        player_h - 12,
                    ):
                        eb.active = False
                        lives -= 1
                        invincible = 90
                        spawn_explosion(explosions, px + player_w / 2.0, py + player_h / 2.0, explosion_life)
                        if lives <= 0:
                            game_over = True
                            queue_sound(game_over_sfx, 6)
                        else:
                            queue_sound(player_hit_sfx, 5)
                        break
                for e in enemies:
                    if not e.active:
                        continue
                    if g.GameLib.rect_overlap(
                        int(e.x),
                        int(e.y),
                        enemy_w,
                        enemy_h,
                        int(px) + 6,
                        int(py) + 6,
                        player_w - 12,
                        player_h - 12,
                    ):
                        e.active = False
                        lives -= 1
                        invincible = 90
                        spawn_explosion(explosions, e.x + enemy_w / 2.0, e.y + enemy_h / 2.0, explosion_life)
                        spawn_explosion(explosions, px + player_w / 2.0, py + player_h / 2.0, explosion_life)
                        if lives <= 0:
                            game_over = True
                            queue_sound(game_over_sfx, 6)
                        else:
                            queue_sound(player_hit_sfx, 5)
                        break

            for ex in explosions:
                if ex.active:
                    ex.timer -= 1
                    if ex.timer <= 0:
                        ex.active = False
        else:
            if game.is_key_pressed(g.KEY_R):
                px = W / 2.0 - player_w / 2.0
                py = H - player_h - 28.0
                for b in bullets:
                    b.active = False
                for e in enemies:
                    e.active = False
                for eb in e_bullets:
                    eb.active = False
                for ex in explosions:
                    ex.active = False
                score, lives, level, kill_count = 0, 3, 1, 0
                spawn_timer = shoot_timer = shoot_sfx_cooldown = 0
                game_over = False
                invincible = 0
                queue_sound(restart_sfx, 1)

        if sfx_to_play:
            game.play_wav(sfx_to_play)

        for s in stars:
            s.y += s.speed
            if s.y > H:
                s.y = 0
                s.x = float(g.GameLib.random(0, W - 1))

        game.clear(g.COLOR_BLACK)

        for s in stars:
            game.set_pixel(int(s.x), int(s.y), s.color)

        for b in bullets:
            if b.active:
                if spr_bullet >= 0:
                    game.draw_sprite_scaled(
                        spr_bullet,
                        int(b.x),
                        int(b.y),
                        player_bullet_w,
                        player_bullet_h,
                        g.SPRITE_COLORKEY,
                    )
                else:
                    game.fill_rect(int(b.x), int(b.y), player_bullet_w, player_bullet_h, g.COLOR_YELLOW)

        for eb in e_bullets:
            if eb.active:
                if spr_bullet >= 0:
                    game.draw_sprite_scaled(
                        spr_bullet,
                        int(eb.x),
                        int(eb.y),
                        enemy_bullet_w,
                        enemy_bullet_h,
                        g.SPRITE_COLORKEY | g.SPRITE_FLIP_V,
                    )
                else:
                    game.fill_rect(int(eb.x), int(eb.y), enemy_bullet_w, enemy_bullet_h, g.COLOR_RED)

        for e in enemies:
            if e.active:
                spr = spr_enemy1 if e.type == 0 else spr_enemy2
                game.draw_sprite_ex(spr, int(e.x), int(e.y), g.SPRITE_COLORKEY)

        for ex in explosions:
            if ex.active:
                if spr_explosion >= 0:
                    frame = (explosion_life - ex.timer) // 4
                    frame = max(0, min(3, frame))
                    game.draw_sprite_frame_scaled(
                        spr_explosion,
                        int(ex.x) - 16,
                        int(ex.y) - 16,
                        32,
                        32,
                        frame,
                        32,
                        32,
                        g.SPRITE_COLORKEY,
                    )
                else:
                    r = explosion_life - ex.timer + 5
                    if ex.timer > 10:
                        c = g.COLOR_WHITE
                    elif ex.timer > 5:
                        c = g.COLOR_YELLOW
                    else:
                        c = g.COLOR_ORANGE
                    game.fill_circle(int(ex.x), int(ex.y), r, c)
                    if r > 3:
                        game.fill_circle(int(ex.x), int(ex.y), r - 3, g.COLOR_RED)

        if invincible == 0 or (invincible // 4) % 2 == 0:
            game.draw_sprite_ex(spr_player, int(px), int(py), g.SPRITE_COLORKEY)

        game.draw_printf(10, 10, g.COLOR_WHITE, f"SCORE: {score}")
        game.draw_printf(W - 100, 10, g.COLOR_GREEN, f"LIVES: {lives}")
        game.draw_printf(W // 2 - 30, 10, g.COLOR_YELLOW, f"LV.{level}")
        game.draw_text(10, H - 15, "Arrows:Move  Space:Shoot", g.COLOR_DARK_GRAY)
        game.draw_printf(10, 40, g.COLOR_WHITE, f"FPS: {game.get_fps():.2f}")

        if game_over:
            game.fill_rect(W // 2 - 120, H // 2 - 50, 240, 100, g.COLOR_DARK_GRAY)
            game.draw_rect(W // 2 - 120, H // 2 - 50, 240, 100, g.COLOR_WHITE)
            game.draw_text_scale(W // 2 - 65, H // 2 - 40, "GAME OVER", g.COLOR_RED, 16, 16)
            game.draw_printf(W // 2 - 55, H // 2, g.COLOR_WHITE, f"Final Score: {score}")
            game.draw_printf(W // 2 - 45, H // 2 + 15, g.COLOR_WHITE, f"Level: {level}")
            game.draw_text(W // 2 - 50, H // 2 + 33, "R to restart", g.COLOR_YELLOW)

        game.update()
        game.wait_frame(60)

    if spr_player >= 0:
        game.free_sprite(spr_player)
    if spr_bullet >= 0:
        game.free_sprite(spr_bullet)
    if spr_explosion >= 0:
        game.free_sprite(spr_explosion)
    if spr_enemy1 >= 0:
        game.free_sprite(spr_enemy1)
    if spr_enemy2 >= 0:
        game.free_sprite(spr_enemy2)


if __name__ == "__main__":
    main()
