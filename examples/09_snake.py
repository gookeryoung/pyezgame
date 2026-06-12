"""09_snake.py - Snake Game

Classic Snake: use arrow keys to control the snake, eat food to grow,
game over if you hit the wall or yourself.
Learn: draw_grid, fill_cell, is_key_pressed, game state machine, timed movement,
       load_sprite, draw_sprite_scaled, play_wav
"""
import os

import pyezgame as g

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

GRID_ROWS = 20
GRID_COLS = 20
CELL_SIZE = 22
MAX_SNAKE = 400




def main() -> None:
    game = g.GameLib()

    grid_w = GRID_COLS * CELL_SIZE
    grid_h = GRID_ROWS * CELL_SIZE
    win_w = grid_w + 160
    win_h = grid_h + 40
    game.open(win_w, win_h, "09 - Snake", True)

    # Load sprite assets
    food_path = g.get_respath("../clib/assets/fruit_apple.png")
    spr_food = game.load_sprite(food_path)

    # Load sound assets
    eat_sfx = g.get_respath("../clib/assets/sound/coin.wav")
    game_over_sfx = g.get_respath("../clib/assets/sound/game_over.wav")

    grid_x, grid_y = 10, 30

    # Snake body: list of (row, col) tuples
    snake = [(10, 10), (10, 9), (10, 8)]
    snake_len = 3

    # Direction: 0=up 1=down 2=left 3=right
    direction = 3
    next_dir = 3

    # Food
    food_r, food_c = 5, 15

    score = 0
    game_over = False
    paused = False

    move_timer = 0.0
    move_interval = 0.15

    while not game.is_closed():
        if game.is_key_pressed(g.KEY_ESCAPE):
            break

        dt = game.get_delta_time()

        if not game_over:
            if game.is_key_pressed(g.KEY_P):
                paused = not paused

            if not paused:
                if game.is_key_pressed(g.KEY_UP) and direction != 1:
                    next_dir = 0
                if game.is_key_pressed(g.KEY_DOWN) and direction != 0:
                    next_dir = 1
                if game.is_key_pressed(g.KEY_LEFT) and direction != 3:
                    next_dir = 2
                if game.is_key_pressed(g.KEY_RIGHT) and direction != 2:
                    next_dir = 3

                move_timer += dt
                if move_timer >= move_interval:
                    move_timer = 0
                    direction = next_dir

                    # Calculate new head position
                    head_r, head_c = snake[0]
                    if direction == 0:
                        head_r -= 1
                    elif direction == 1:
                        head_r += 1
                    elif direction == 2:
                        head_c -= 1
                    elif direction == 3:
                        head_c += 1

                    # Wall collision
                    if head_r < 0 or head_r >= GRID_ROWS or head_c < 0 or head_c >= GRID_COLS:
                        game_over = True
                        game.play_wav(game_over_sfx, 1, 1000)
                    else:
                        # Self collision
                        if (head_r, head_c) in snake[:snake_len]:
                            game_over = True
                            game.play_wav(game_over_sfx, 1, 1000)

                    if not game_over:
                        ate = (head_r == food_r and head_c == food_c)

                        if not ate:
                            # Move: shift body, drop tail
                            snake.insert(0, (head_r, head_c))
                            snake.pop()
                        else:
                            # Grow
                            snake.insert(0, (head_r, head_c))
                            snake_len += 1
                            score += 10
                            if move_interval > 0.06:
                                move_interval -= 0.003

                            # New food (ensure not on snake)
                            while True:
                                food_r = g.GameLib.random(0, GRID_ROWS - 1)
                                food_c = g.GameLib.random(0, GRID_COLS - 1)
                                if (food_r, food_c) not in snake[:snake_len]:
                                    break
                            game.play_wav(eat_sfx, 1, 800)
        else:
            if game.is_key_pressed(g.KEY_R):
                snake = [(10, 10), (10, 9), (10, 8)]
                snake_len = 3
                direction = 3
                next_dir = 3
                food_r, food_c = 5, 15
                score = 0
                move_interval = 0.15
                game_over = False

        # --- Drawing ---
        game.clear(g.COLOR_BLACK)

        game.draw_text_scale(grid_x, 5, "SNAKE", g.COLOR_GREEN, 16, 16)
        game.draw_grid(grid_x, grid_y, GRID_ROWS, GRID_COLS, CELL_SIZE, g.COLOR_DARK_GRAY)

        # Draw food (use sprite if loaded)
        if spr_food >= 0:
            fx = grid_x + food_c * CELL_SIZE + 1
            fy = grid_y + food_r * CELL_SIZE + 1
            game.draw_sprite_scaled(
                spr_food, fx, fy, CELL_SIZE - 2, CELL_SIZE - 2, g.SPRITE_COLORKEY,
            )
        else:
            game.fill_cell(grid_x, grid_y, food_r, food_c, CELL_SIZE, g.COLOR_RED)

        for i in range(min(snake_len, len(snake))):
            sr, sc = snake[i]
            c = g.COLOR_GREEN if i == 0 else g.COLOR_DARK_GREEN
            game.fill_cell(grid_x, grid_y, sr, sc, CELL_SIZE, c)

        # Right info panel
        info_x = grid_x + grid_w + 15
        game.draw_text(info_x, 40, "Score:", g.COLOR_WHITE)
        game.draw_number(info_x, 55, score, g.COLOR_GOLD)

        game.draw_text(info_x, 85, "Length:", g.COLOR_WHITE)
        game.draw_number(info_x, 100, snake_len, g.COLOR_CYAN)

        game.draw_text(info_x, 140, "Controls:", g.COLOR_GRAY)
        game.draw_text(info_x, 158, "Arrows", g.COLOR_LIGHT_GRAY)
        game.draw_text(info_x, 172, "P: Pause", g.COLOR_LIGHT_GRAY)

        if paused and not game_over:
            game.fill_rect(grid_x + grid_w // 2 - 50, grid_y + grid_h // 2 - 15,
                           100, 30, g.COLOR_DARK_GRAY)
            game.draw_text(grid_x + grid_w // 2 - 30, grid_y + grid_h // 2 - 7,
                           "PAUSED", g.COLOR_YELLOW)

        if game_over:
            cx = grid_x + grid_w // 2
            cy = grid_y + grid_h // 2
            game.fill_rect(cx - 80, cy - 30, 160, 70, g.COLOR_DARK_GRAY)
            game.draw_rect(cx - 80, cy - 30, 160, 70, g.COLOR_WHITE)
            game.draw_text_scale(cx - 65, cy - 22, "GAME OVER", g.COLOR_RED, 8, 8)
            game.draw_printf(cx - 50, cy + 2, g.COLOR_WHITE, f"Score: {score}")
            game.draw_text(cx - 55, cy + 20, "R to restart", g.COLOR_YELLOW)

        game.update()
        game.wait_frame(60)

    if spr_food >= 0:
        game.free_sprite(spr_food)


if __name__ == "__main__":
    main()
