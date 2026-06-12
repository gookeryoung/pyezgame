"""08_breakout.py - Breakout

Classic Breakout: bounce the ball with paddle, destroy all bricks to win.
Learn: in-depth collision detection, multi-object management, game state
"""
import os

import pyezgame as g

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

BRICK_ROWS = 6
BRICK_COLS = 10
BRICK_W = 58
BRICK_H = 18
BRICK_GAP = 4
BRICK_OFFSET_X = 12
BRICK_OFFSET_Y = 50


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


def main() -> None:
    game = g.GameLib()
    game.open(640, 480, "08 - Breakout", True)

    launch_sfx = choose_existing_path("../clib/assets/sound/jump.wav", "assets/sound/jump.wav")
    bounce_sfx = choose_existing_path("../clib/assets/sound/hit.wav", "assets/sound/hit.wav")
    brick_row_sfx = [
        choose_existing_path("../clib/assets/sound/note_do_high.wav", "assets/sound/note_do_high.wav"),
        choose_existing_path("../clib/assets/sound/note_si.wav", "assets/sound/note_si.wav"),
        choose_existing_path("../clib/assets/sound/note_la.wav", "assets/sound/note_la.wav"),
        choose_existing_path("../clib/assets/sound/note_sol.wav", "assets/sound/note_sol.wav"),
        choose_existing_path("../clib/assets/sound/note_fa.wav", "assets/sound/note_fa.wav"),
        choose_existing_path("../clib/assets/sound/note_mi.wav", "assets/sound/note_mi.wav"),
    ]
    lose_life_sfx = choose_existing_path("../clib/assets/sound/explosion.wav", "assets/sound/explosion.wav")
    restart_sfx = choose_existing_path("../clib/assets/sound/click.wav", "assets/sound/click.wav")
    game_over_sfx = choose_existing_path("../clib/assets/sound/game_over.wav", "assets/sound/game_over.wav")
    win_sfx = choose_existing_path("../clib/assets/sound/victory.wav", "assets/sound/victory.wav")

    brick_colors = [g.COLOR_RED, g.COLOR_ORANGE, g.COLOR_YELLOW,
                    g.COLOR_GREEN, g.COLOR_CYAN, g.COLOR_PURPLE]

    pad_w, pad_h = 80, 12
    pad_x, pad_y = 280, 450

    ball_x, ball_y = 320.0, 430.0
    ball_vx, ball_vy = 3.0, -4.0
    ball_r = 5

    score, lives = 0, 3
    bricks = [[True] * BRICK_COLS for _ in range(BRICK_ROWS)]
    total_bricks = BRICK_ROWS * BRICK_COLS
    started = False
    game_over = False
    game_win = False

    while not game.is_closed():
        sfx_to_play = None
        if game.is_key_pressed(g.KEY_ESCAPE):
            break

        if not game_over and not game_win:
            if game.is_key_down(g.KEY_LEFT):
                pad_x -= 6
            if game.is_key_down(g.KEY_RIGHT):
                pad_x += 6
            pad_x = max(0, min(pad_x, game.get_width() - pad_w))

            if not started:
                ball_x = float(pad_x + pad_w // 2)
                ball_y = float(pad_y - ball_r - 1)
                if game.is_key_pressed(g.KEY_SPACE):
                    started = True
                    ball_vx, ball_vy = 3.0, -4.0
                    sfx_to_play = launch_sfx
            else:
                ball_x += ball_vx
                ball_y += ball_vy

                if ball_x - ball_r < 0:
                    ball_x = float(ball_r)
                    ball_vx = -ball_vx
                    if not sfx_to_play:
                        sfx_to_play = bounce_sfx
                if ball_x + ball_r > game.get_width():
                    ball_x = float(game.get_width() - ball_r)
                    ball_vx = -ball_vx
                    if not sfx_to_play:
                        sfx_to_play = bounce_sfx
                if ball_y - ball_r < 0:
                    ball_y = float(ball_r)
                    ball_vy = -ball_vy
                    if not sfx_to_play:
                        sfx_to_play = bounce_sfx
                if ball_y + ball_r > game.get_height():
                    lives -= 1
                    if lives <= 0:
                        game_over = True
                        sfx_to_play = game_over_sfx
                    else:
                        started = False
                        ball_vx, ball_vy = 3.0, -4.0
                        sfx_to_play = lose_life_sfx

                # Paddle collision
                if (ball_vy > 0 and
                        ball_x + ball_r > pad_x and ball_x - ball_r < pad_x + pad_w and
                        pad_y <= ball_y + ball_r <= pad_y + pad_h + 4):
                    ball_vy = -ball_vy
                    ball_y = float(pad_y - ball_r)
                    hit_pos = (ball_x - pad_x) / pad_w
                    ball_vx = (hit_pos - 0.5) * 8.0
                    if not sfx_to_play:
                        sfx_to_play = bounce_sfx

                # Brick collision
                hit_brick = False
                for r in range(BRICK_ROWS):
                    if hit_brick:
                        break
                    for c in range(BRICK_COLS):
                        if not bricks[r][c]:
                            continue
                        bx = BRICK_OFFSET_X + c * (BRICK_W + BRICK_GAP)
                        by = BRICK_OFFSET_Y + r * (BRICK_H + BRICK_GAP)

                        if (ball_x + ball_r > bx and ball_x - ball_r < bx + BRICK_W and
                                ball_y + ball_r > by and ball_y - ball_r < by + BRICK_H):
                            bricks[r][c] = False
                            total_bricks -= 1
                            score += 10 * (BRICK_ROWS - r)

                            overlap_left = (ball_x + ball_r) - bx
                            overlap_right = (bx + BRICK_W) - (ball_x - ball_r)
                            overlap_top = (ball_y + ball_r) - by
                            overlap_bottom = (by + BRICK_H) - (ball_y - ball_r)
                            min_overlap_x = min(overlap_left, overlap_right)
                            min_overlap_y = min(overlap_top, overlap_bottom)

                            if min_overlap_x < min_overlap_y:
                                ball_vx = -ball_vx
                            else:
                                ball_vy = -ball_vy

                            if total_bricks <= 0:
                                game_win = True
                                sfx_to_play = win_sfx
                            else:
                                sfx_to_play = brick_row_sfx[r]
                            hit_brick = True
                            break
        else:
            if game.is_key_pressed(g.KEY_R):
                bricks = [[True] * BRICK_COLS for _ in range(BRICK_ROWS)]
                total_bricks = BRICK_ROWS * BRICK_COLS
                score, lives = 0, 3
                pad_x = 280
                started = False
                game_over = False
                game_win = False
                sfx_to_play = restart_sfx

        if sfx_to_play:
            game.play_wav(sfx_to_play)

        game.clear(g.COLOR_BLACK)

        game.draw_printf(10, 10, g.COLOR_WHITE, f"Score: {score}")
        game.draw_printf(10, 25, g.COLOR_GREEN, f"Lives: {lives}")
        game.draw_printf(game.get_width() - 130, 10, g.COLOR_GRAY, f"Bricks: {total_bricks}")

        for r in range(BRICK_ROWS):
            for c in range(BRICK_COLS):
                if not bricks[r][c]:
                    continue
                bx = BRICK_OFFSET_X + c * (BRICK_W + BRICK_GAP)
                by = BRICK_OFFSET_Y + r * (BRICK_H + BRICK_GAP)
                game.fill_rect(bx, by, BRICK_W, BRICK_H, brick_colors[r])
                game.draw_rect(bx, by, BRICK_W, BRICK_H, g.COLOR_WHITE)

        game.fill_rect(pad_x, pad_y, pad_w, pad_h, g.COLOR_WHITE)
        game.fill_circle(int(ball_x), int(ball_y), ball_r, g.COLOR_WHITE)

        if not started and not game_over and not game_win:
            game.draw_text(240, 420, "SPACE to launch", g.COLOR_YELLOW)

        if game_over:
            game.fill_rect(200, 200, 240, 80, g.COLOR_DARK_GRAY)
            game.draw_rect(200, 200, 240, 80, g.COLOR_WHITE)
            game.draw_text_scale(230, 210, "GAME OVER", g.COLOR_RED, 16, 16)
            game.draw_printf(260, 245, g.COLOR_WHITE, f"Score: {score}")
            game.draw_text(245, 262, "R to restart", g.COLOR_YELLOW)
        if game_win:
            game.fill_rect(200, 200, 240, 80, g.COLOR_DARK_GRAY)
            game.draw_rect(200, 200, 240, 80, g.COLOR_WHITE)
            game.draw_text_scale(240, 210, "YOU WIN!", g.COLOR_GREEN, 16, 16)
            game.draw_printf(260, 245, g.COLOR_WHITE, f"Score: {score}")
            game.draw_text(245, 262, "R to restart", g.COLOR_YELLOW)

        game.update()
        game.wait_frame(60)


if __name__ == "__main__":
    main()
