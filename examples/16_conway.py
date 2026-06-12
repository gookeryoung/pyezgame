"""16_conway.py - Conway's Game of Life

A cellular automaton where cells live or die based on their neighbours.
Click to toggle cells, press SPACE to step, P to pause, R to reset.
Learn: draw_grid, fill_cell, mouse input, game state, timer-based updates
"""
from __future__ import annotations

import pyezgame as g

FPS = 60
GRID_ROWS = 40
GRID_COLS = 50
CELL_SIZE = 12
UPDATE_INTERVAL = 0.01  # seconds between generations


def count_neighbours(cells: list[list[int]], row: int, col: int) -> int:
    """Count alive neighbours with toroidal (wrap-around) edges."""
    total = 0
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            r = (row + dr) % GRID_ROWS
            c = (col + dc) % GRID_COLS
            total += cells[r][c]
    return total


def make_grid() -> list[list[int]]:
    """Create a random initial grid."""
    return [
        [g.GameLib.random(0, 3) // 3 for _ in range(GRID_COLS)]  # ~25% alive
        for _ in range(GRID_ROWS)
    ]


def step(cells: list[list[int]]) -> list[list[int]]:
    """Compute next generation using Conway's rules."""
    new = [[0] * GRID_COLS for _ in range(GRID_ROWS)]
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            n = count_neighbours(cells, r, c)
            if cells[r][c] == 1:
                # Alive: survive with 2 or 3 neighbours
                new[r][c] = 1 if n in (2, 3) else 0
            else:
                # Dead: born with exactly 3 neighbours
                new[r][c] = 1 if n == 3 else 0
    return new


def count_population(cells: list[list[int]]) -> int:
    return sum(cells[r][c] for r in range(GRID_ROWS) for c in range(GRID_COLS))


def main() -> None:
    game = g.GameLib()

    grid_w = GRID_COLS * CELL_SIZE
    grid_h = GRID_ROWS * CELL_SIZE
    win_w = grid_w + 170
    win_h = grid_h + 40
    game.open(win_w, win_h, "16 - Conway's Game of Life", True)

    grid_x, grid_y = 10, 30
    cells = make_grid()
    generation = 0
    population = count_population(cells)

    paused = False
    single_step = False
    timer = 0.0

    while not game.is_closed():
        if game.is_key_pressed(g.KEY_ESCAPE):
            break

        dt = game.get_delta_time()

        # --- Input ---
        if game.is_key_pressed(g.KEY_P):
            paused = not paused

        if game.is_key_pressed(g.KEY_R):
            cells = make_grid()
            generation = 0
            population = count_population(cells)
            timer = 0.0
            paused = False

        if game.is_key_pressed(g.KEY_SPACE):
            single_step = True

        # Mouse click to toggle cells
        mx, my = game.get_mouse_x(), game.get_mouse_y()
        if game.is_mouse_pressed(g.MOUSE_LEFT):
            col = (mx - grid_x) // CELL_SIZE
            row = (my - grid_y) // CELL_SIZE
            if 0 <= row < GRID_ROWS and 0 <= col < GRID_COLS:
                cells[row][col] = 1 - cells[row][col]
                population = count_population(cells)

        # --- Update ---
        if not paused or single_step:
            timer += dt
            if timer >= UPDATE_INTERVAL:
                timer = 0.0
                cells = step(cells)
                generation += 1
                population = count_population(cells)
            single_step = False

        # --- Drawing ---
        game.clear(g.COLOR_BLACK)

        # Title
        game.draw_text_scale(grid_x, 5, "CONWAY'S GAME OF LIFE", g.COLOR_GREEN, 8, 8)

        # Grid
        game.draw_grid(grid_x, grid_y, GRID_ROWS, GRID_COLS, CELL_SIZE, g.COLOR_DARK_GRAY)

        # Draw alive cells
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                if cells[r][c] == 1:
                    game.fill_cell(grid_x, grid_y, r, c, CELL_SIZE, g.COLOR_GREEN)

        # Right info panel
        info_x = grid_x + grid_w + 15
        game.draw_text(info_x, 40, "Generation:", g.COLOR_WHITE)
        game.draw_number(info_x, 55, generation, g.COLOR_GOLD)

        game.draw_text(info_x, 80, "Population:", g.COLOR_WHITE)
        game.draw_number(info_x, 95, population, g.COLOR_CYAN)

        game.draw_text(info_x, 140, "Controls:", g.COLOR_GRAY)
        game.draw_text(info_x, 158, "Click: Toggle", g.COLOR_LIGHT_GRAY)
        game.draw_text(info_x, 172, "SPACE: Step", g.COLOR_LIGHT_GRAY)
        game.draw_text(info_x, 186, "P: Pause", g.COLOR_LIGHT_GRAY)
        game.draw_text(info_x, 200, "R: Reset", g.COLOR_LIGHT_GRAY)
        game.draw_text(info_x, 214, "ESC: Quit", g.COLOR_LIGHT_GRAY)

        # Status indicator
        status = "PAUSED" if paused else "RUNNING"
        status_color = g.COLOR_YELLOW if paused else g.COLOR_GREEN
        game.draw_text(info_x, 240, "Status:", g.COLOR_WHITE)
        game.draw_text(info_x, 255, status, status_color)
        game.draw_printf(info_x, 270, g.COLOR_WHITE, f"FPS: {game.get_fps():.2f}")

        # Pause overlay
        if paused:
            cx = grid_x + grid_w // 2
            cy = grid_y + grid_h // 2
            game.fill_rect(cx - 55, cy - 12, 110, 24, g.COLOR_DARK_GRAY)
            game.draw_text(cx - 42, cy - 5, "PAUSED", g.COLOR_YELLOW)

        game.update()
        game.wait_frame(FPS)


if __name__ == "__main__":
    main()
