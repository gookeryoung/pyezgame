"""17_tetris.py - Tetris (Russian Block)

A classic Tetris game with modern features: ghost piece, next preview,
hold piece, wall kicks, scoring, levels, and line clear effects.
Learn: grid-based game, piece rotation, collision, timer-based updates,
       state machine, DAS input handling
"""

from __future__ import annotations

from dataclasses import dataclass, field

import pyezgame as g

# --- Board Config ---
CELL = 24
COLS = 10
ROWS = 20
BOARD_W = COLS * CELL
BOARD_H = ROWS * CELL
SIDEBAR = 170
WIN_W = BOARD_W + SIDEBAR + 30
WIN_H = BOARD_H + 40
BOARD_X = 10
BOARD_Y = 20
FPS = 60

# --- Colors (ARGB) ---
BG = g.COLOR_RGB(18, 18, 30)
BOARD_BG = g.COLOR_RGB(10, 10, 22)
GRID_COL = g.COLOR_RGB(30, 30, 55)
BORDER = g.COLOR_RGB(60, 60, 100)
SIDEBAR_BG = g.COLOR_RGB(22, 22, 40)
TEXT_COL = g.COLOR_RGB(220, 220, 240)
ACCENT = g.COLOR_RGB(100, 140, 255)
DIM_TEXT = g.COLOR_RGB(140, 140, 180)
GHOST_ALPHA = g.COLOR_ARGB(60, 180, 180, 200)

# piece type -> (main, light, dark, ghost)
PIECE_COLORS: dict[str, tuple[int, int, int, int]] = {
    "I": (
        g.COLOR_RGB(0, 220, 255),
        g.COLOR_RGB(100, 240, 255),
        g.COLOR_RGB(0, 160, 200),
        g.COLOR_ARGB(50, 0, 220, 255),
    ),
    "O": (
        g.COLOR_RGB(255, 220, 50),
        g.COLOR_RGB(255, 240, 130),
        g.COLOR_RGB(200, 170, 30),
        g.COLOR_ARGB(50, 255, 220, 50),
    ),
    "T": (
        g.COLOR_RGB(180, 60, 255),
        g.COLOR_RGB(220, 130, 255),
        g.COLOR_RGB(130, 30, 200),
        g.COLOR_ARGB(50, 180, 60, 255),
    ),
    "S": (
        g.COLOR_RGB(50, 255, 100),
        g.COLOR_RGB(130, 255, 160),
        g.COLOR_RGB(30, 200, 70),
        g.COLOR_ARGB(50, 50, 255, 100),
    ),
    "Z": (
        g.COLOR_RGB(255, 60, 80),
        g.COLOR_RGB(255, 130, 140),
        g.COLOR_RGB(200, 30, 50),
        g.COLOR_ARGB(50, 255, 60, 80),
    ),
    "J": (
        g.COLOR_RGB(60, 100, 255),
        g.COLOR_RGB(130, 160, 255),
        g.COLOR_RGB(30, 60, 200),
        g.COLOR_ARGB(50, 60, 100, 255),
    ),
    "L": (
        g.COLOR_RGB(255, 150, 30),
        g.COLOR_RGB(255, 190, 100),
        g.COLOR_RGB(200, 110, 20),
        g.COLOR_ARGB(50, 255, 150, 30),
    ),
}

GARBAGE_COL = g.COLOR_RGB(80, 80, 80)

# --- Shapes: 4 rotation states per piece ---
SHAPES: dict[str, list[list[tuple[int, int]]]] = {
    "I": [
        [(0, 0), (1, 0), (2, 0), (3, 0)],
        [(0, 0), (0, 1), (0, 2), (0, 3)],
        [(0, 0), (1, 0), (2, 0), (3, 0)],
        [(0, 0), (0, 1), (0, 2), (0, 3)],
    ],
    "O": [[(0, 0), (1, 0), (0, 1), (1, 1)]] * 4,
    "T": [
        [(0, 0), (1, 0), (2, 0), (1, 1)],
        [(0, 0), (0, 1), (0, 2), (1, 1)],
        [(1, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (0, 1)],
    ],
    "S": [
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        [(0, 0), (0, 1), (1, 1), (1, 2)],
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        [(0, 0), (0, 1), (1, 1), (1, 2)],
    ],
    "Z": [
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(1, 0), (0, 1), (1, 1), (0, 2)],
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(1, 0), (0, 1), (1, 1), (0, 2)],
    ],
    "J": [
        [(0, 0), (0, 1), (1, 1), (2, 1)],
        [(0, 0), (1, 0), (0, 1), (0, 2)],
        [(0, 0), (1, 0), (2, 0), (2, 1)],
        [(1, 0), (1, 1), (0, 2), (1, 2)],
    ],
    "L": [
        [(2, 0), (0, 1), (1, 1), (2, 1)],
        [(0, 0), (0, 1), (0, 2), (1, 2)],
        [(0, 0), (1, 0), (2, 0), (0, 1)],
        [(0, 0), (1, 0), (1, 1), (1, 2)],
    ],
}

# --- Wall Kick Data (SRS) ---
WALL_KICKS: dict[str, dict[tuple[int, int], list[tuple[int, int]]]] = {
    "default": {
        (0, 1): [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
        (1, 0): [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
        (1, 2): [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
        (2, 1): [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
        (2, 3): [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
        (3, 2): [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
        (3, 0): [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
        (0, 3): [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
    },
    "I": {
        (0, 1): [(0, 0), (-2, 0), (1, 0), (-2, 1), (1, -2)],
        (1, 0): [(0, 0), (2, 0), (-1, 0), (2, -1), (-1, 2)],
        (1, 2): [(0, 0), (-1, 0), (2, 0), (-1, -2), (2, 1)],
        (2, 1): [(0, 0), (1, 0), (-2, 0), (1, 2), (-2, -1)],
        (2, 3): [(0, 0), (2, 0), (-1, 0), (2, -1), (-1, 2)],
        (3, 2): [(0, 0), (-2, 0), (1, 0), (-2, 1), (1, -2)],
        (3, 0): [(0, 0), (1, 0), (-2, 0), (1, 2), (-2, -1)],
        (0, 3): [(0, 0), (-1, 0), (2, 0), (-1, -2), (2, 1)],
    },
}

PIECE_NAMES = list(SHAPES.keys())


# --- Piece ---
@dataclass
class Piece:
    type: str
    rot: int
    x: int
    y: int
    colors: tuple[int, int, int, int]

    def cells(self) -> list[tuple[int, int]]:
        return [(self.x + dx, self.y + dy) for dx, dy in SHAPES[self.type][self.rot]]

    def cells_offset(self, xo: int, yo: int) -> list[tuple[int, int]]:
        return [(self.x + dx + xo, self.y + dy + yo) for dx, dy in SHAPES[self.type][self.rot]]


# --- Bag Randomizer (7-bag) ---
@dataclass
class BagGen:
    bag: list[str] = field(default_factory=list)
    queue: list[str] = field(default_factory=list)

    def _fill_bag(self) -> None:
        self.bag = list(PIECE_NAMES)
        for i in range(len(self.bag) - 1, 0, -1):
            j = g.GameLib.random(0, i)
            self.bag[i], self.bag[j] = self.bag[j], self.bag[i]

    def _next(self) -> str:
        if not self.bag:
            self._fill_bag()
        return self.bag.pop()

    def refill(self, target: int = 5) -> None:
        while len(self.queue) < target:
            self.queue.append(self._next())

    def pop(self) -> str:
        if not self.queue:
            self.refill()
        return self.queue.pop(0)

    def peek(self, idx: int = 0) -> str:
        while len(self.queue) <= idx:
            self.queue.append(self._next())
        return self.queue[idx]

    def clear(self) -> None:
        self.bag.clear()
        self.queue.clear()


# --- Helpers ---
def get_fall_speed(level: int) -> float:
    return max(0.05, 1.0 - (level - 1) * 0.08)


def draw_block(game: g.GameLib, px: int, py: int, main: int, light: int, dark: int) -> None:
    """Draw a single block cell with simple shading."""
    game.fill_rect(px, py, CELL, CELL, main)
    # top highlight
    game.draw_line(px, py, px + CELL - 1, py, light)
    game.draw_line(px, py, px, py + CELL - 1, light)
    # bottom shadow
    game.draw_line(px + CELL - 1, py, px + CELL - 1, py + CELL - 1, dark)
    game.draw_line(px, py + CELL - 1, px + CELL - 1, py + CELL - 1, dark)
    # inner highlight
    game.fill_rect(px + 2, py + 2, CELL - 6, max(1, (CELL - 6) // 4), g.COLOR_ARGB(40, 255, 255, 255))


def draw_mini_piece(game: g.GameLib, ptype: str | None, cx: int, cy: int, cs: int = 14) -> None:
    """Draw a small piece preview centred at (cx, cy)."""
    if ptype is None:
        return
    shape = SHAPES[ptype][0]
    main, light, _dark, _ghost = PIECE_COLORS[ptype]
    min_x = min(dx for dx, _ in shape)
    max_x = max(dx for dx, _ in shape)
    min_y = min(dy for _, dy in shape)
    max_y = max(dy for _, dy in shape)
    w = (max_x - min_x + 1) * cs
    h = (max_y - min_y + 1) * cs
    ox = cx - w // 2
    oy = cy - h // 2
    for dx, dy in shape:
        bx = ox + (dx - min_x) * cs
        by = oy + (dy - min_y) * cs
        game.fill_rect(bx, by, cs, cs, main)
        game.draw_rect(bx, by, cs, cs, light)


# --- Game ---
def main() -> None:
    game = g.GameLib()
    _ = game.open(WIN_W, WIN_H, "17 - Tetris", True)

    # --- state ---
    board: list[list[str | None]] = [[None] * COLS for _ in range(ROWS)]
    gen = BagGen()
    current: Piece | None = None
    next_piece: Piece | None = None
    held: Piece | None = None
    can_hold = True
    score = 0
    level = 1
    lines = 0
    game_over = False
    paused = False

    fall_timer = 0.0
    fall_speed = get_fall_speed(1)
    lock_timer = 0.0
    lock_delay = 0.5
    is_locking = False

    combo = 0
    notif_text = ""
    notif_timer = 0.0

    # clearing animation
    clear_rows: list[int] = []
    clear_timer = 0.0
    clear_dur = 0.4
    clearing = False

    # DAS (Delayed Auto Shift)
    das_dir = 0
    das_timer = 0.0
    das_delay = 0.17
    das_repeat = 0.05
    das_active = False
    down_held = False

    def spawn() -> tuple[Piece, Piece]:
        nonlocal current, next_piece, can_hold, is_locking, lock_timer
        nonlocal fall_timer, fall_speed, das_dir, das_timer, das_active, down_held
        gen.refill(5)
        if next_piece is None:
            ptype = gen.pop()
            current = Piece(ptype, 0, 3, 0, PIECE_COLORS[ptype])
            next_ptype = gen.pop()
            next_piece = Piece(next_ptype, 0, 3, 0, PIECE_COLORS[next_ptype])
        else:
            current = next_piece
            next_ptype = gen.pop()
            next_piece = Piece(next_ptype, 0, 3, 0, PIECE_COLORS[next_ptype])
        can_hold = True
        is_locking = False
        lock_timer = 0.0
        # reset fall state so new piece gets a fresh start
        fall_speed = get_fall_speed(level)
        fall_timer = 0.0
        # reset DAS / soft-drop state
        das_dir = 0
        das_timer = 0.0
        das_active = False
        down_held = False
        # check game over
        for x, y in current.cells():
            if y < 0 or x < 0 or x >= COLS or y >= ROWS:
                nonlocal game_over
                game_over = True
                return current, next_piece
            if board[y][x] is not None:
                game_over = True
                return current, next_piece
        return current, next_piece

    def is_valid(piece: Piece, xo: int = 0, yo: int = 0, rot: int | None = None) -> bool:
        if rot is not None:
            cl = [(piece.x + dx + xo, piece.y + dy + yo) for dx, dy in SHAPES[piece.type][rot]]
        else:
            cl = piece.cells_offset(xo, yo)
        for x, y in cl:
            if x < 0 or x >= COLS or y >= ROWS:
                return False
            if y >= 0 and board[y][x] is not None:
                return False
        return True

    def do_move(dx: int, dy: int) -> bool:
        assert current is not None
        nonlocal is_locking, lock_timer
        if is_valid(current, dx, dy):
            current.x += dx
            current.y += dy
            if is_locking and dy == 0:
                lock_timer = 0
            return True
        return False

    def do_rotate(direction: int = 1) -> bool:
        assert current is not None
        nonlocal is_locking, lock_timer
        old = current.rot
        new = (old + direction) % 4
        kicks = WALL_KICKS["I" if current.type == "I" else "default"]
        kick_list = kicks.get((old, new), [(0, 0)])
        for dx, dy in kick_list:
            if is_valid(current, dx, dy, new):
                current.x += dx
                current.y += dy
                current.rot = new
                if is_locking:
                    lock_timer = 0
                return True
        return False

    def ghost_y() -> int:
        assert current is not None
        gy = current.y
        while True:
            ok = True
            for dx, dy in SHAPES[current.type][current.rot]:
                nx = current.x + dx
                ny = gy + dy + 1
                if nx < 0 or nx >= COLS or ny >= ROWS or (ny >= 0 and board[ny][nx] is not None):
                    ok = False
                    break
            if not ok:
                break
            gy += 1
        return gy

    def hard_drop() -> None:
        assert current is not None
        nonlocal score
        dist = 0
        while is_valid(current, 0, 1):
            current.y += 1
            dist += 1
        score += dist * 2
        do_lock()

    def do_lock() -> None:
        nonlocal current, next_piece, score, level, lines, combo, clearing, clear_timer
        nonlocal clear_rows, notif_text, notif_timer
        assert current is not None
        for x, y in current.cells():
            if 0 <= y < ROWS and 0 <= x < COLS:
                board[y][x] = current.type

        full = [r for r in range(ROWS) if all(board[r][c] is not None for c in range(COLS))]
        n = len(full)

        if n > 0:
            clear_rows = full
            clear_timer = 0.0
            clearing = True
            combo += 1
            base = {1: 100, 2: 300, 3: 500, 4: 800}.get(n, 0)
            bonus = combo * 50 if combo > 1 else 0
            score += (base + bonus) * level
            lines += n
            level = lines // 10 + 1
            if n == 4:
                notif_text = "QUAD!"
                notif_timer = 1.5
            elif combo >= 3:
                notif_text = f"COMBO x{combo}"
                notif_timer = 1.5
        else:
            combo = 0
            current, next_piece = spawn()

    def remove_cleared() -> None:
        nonlocal current, next_piece, clearing, clear_rows, board
        cleared_set = set(clear_rows)
        remaining = [board[r] for r in range(ROWS) if r not in cleared_set]
        empty: list[str | None] = [None] * COLS
        board = [list(empty) for _ in range(len(clear_rows))] + remaining
        clear_rows.clear()
        clearing = False
        current, next_piece = spawn()

    def do_hold() -> None:
        nonlocal current, next_piece, held, can_hold, is_locking, lock_timer
        assert current is not None
        if not can_hold:
            return
        can_hold = False
        is_locking = False
        lock_timer = 0.0
        if held is None:
            held = Piece(current.type, 0, 3, 0, current.colors)
            current, next_piece = spawn()
        else:
            old = held.type
            held = Piece(current.type, 0, 3, 0, current.colors)
            current = Piece(old, 0, 3, 0, PIECE_COLORS[old])

    def reset() -> None:
        nonlocal current, board, next_piece, held, can_hold
        nonlocal score, level, lines, game_over, paused
        nonlocal fall_timer, fall_speed, lock_timer, is_locking
        nonlocal combo, notif_text, notif_timer
        nonlocal clear_rows, clearing, clear_timer
        nonlocal das_dir, das_timer, das_active, down_held
        board = [[None] * COLS for _ in range(ROWS)]
        current = None
        next_piece = None
        held = None
        can_hold = True
        score = 0
        level = 1
        lines = 0
        game_over = False
        paused = False
        fall_timer = 0.0
        fall_speed = get_fall_speed(1)
        lock_timer = 0.0
        is_locking = False
        combo = 0
        notif_text = ""
        notif_timer = 0.0
        clear_rows = []
        clearing = False
        clear_timer = 0.0
        das_dir = 0
        das_timer = 0.0
        das_active = False
        down_held = False
        gen.clear()
        current, next_piece = spawn()

    # initial spawn
    current, next_piece = spawn()

    # === Main Loop ===
    while not game.is_closed():
        if game.is_key_pressed(g.KEY_ESCAPE):
            break

        dt = game.get_delta_time()

        # --- Input ---
        if game.is_key_pressed(g.KEY_P):
            paused = not paused

        if game_over:
            if game.is_key_pressed(g.KEY_R):
                reset()
        elif not paused:
            # DAS
            if game.is_key_down(g.KEY_LEFT):
                if das_dir != -1:
                    das_dir = -1
                    das_timer = 0.0
                    das_active = False
                    if not clearing:
                        _ = do_move(-1, 0)
            elif game.is_key_down(g.KEY_RIGHT):
                if das_dir != 1:
                    das_dir = 1
                    das_timer = 0.0
                    das_active = False
                    if not clearing:
                        _ = do_move(1, 0)
            else:
                das_dir = 0
                das_active = False

            if das_dir != 0 and not clearing:
                das_timer += dt
                if not das_active and das_timer >= das_delay:
                    das_active = True
                    das_timer = 0.0
                if das_active and das_timer >= das_repeat:
                    _ = do_move(das_dir, 0)
                    das_timer = 0.0

            if game.is_key_pressed(g.KEY_UP) and not clearing:
                _ = do_rotate(1)
            if game.is_key_pressed(g.KEY_Z) and not clearing:
                _ = do_rotate(-1)

            if game.is_key_down(g.KEY_DOWN):
                down_held = True
            if game.is_key_released(g.KEY_DOWN):
                down_held = False

            if game.is_key_pressed(g.KEY_DOWN) and not clearing and do_move(0, 1):
                score += 1
                fall_timer = 0.0

            if game.is_key_pressed(g.KEY_SPACE) and not clearing:
                hard_drop()

            if game.is_key_pressed(g.KEY_C) and not clearing:
                do_hold()

        # --- Update ---
        if not paused and not game_over and not clearing:
            fall_timer += dt
            if fall_timer >= fall_speed:
                fall_timer = 0.0
                if do_move(0, 1):
                    if down_held:
                        score += 1
                else:
                    if not is_locking:
                        is_locking = True
                        lock_timer = 0.0

            if is_locking:
                lock_timer += dt
                if is_valid(current, 0, 1):
                    is_locking = False
                    lock_timer = 0.0
                elif lock_timer >= lock_delay:
                    do_lock()

            # soft drop while held
            if down_held:
                fall_timer += dt * 4

        # clearing animation
        if clearing:
            clear_timer += dt
            if clear_timer >= clear_dur:
                remove_cleared()

        if notif_timer > 0:
            notif_timer -= dt

        # --- Drawing ---
        game.clear(BG)

        # board background
        game.fill_rect(BOARD_X - 2, BOARD_Y - 2, BOARD_W + 4, BOARD_H + 4, BOARD_BG)
        game.draw_rect(BOARD_X - 2, BOARD_Y - 2, BOARD_W + 4, BOARD_H + 4, BORDER)

        # grid lines
        game.draw_grid(BOARD_X, BOARD_Y, ROWS, COLS, CELL, GRID_COL)

        # fixed blocks
        for r in range(ROWS):
            for c in range(COLS):
                if board[r][c] is not None:
                    if clearing and r in clear_rows:
                        flash = int(clear_timer / clear_dur * 3) % 2
                        pt = board[r][c]
                        clr = PIECE_COLORS[pt][0] if pt and pt in PIECE_COLORS else GARBAGE_COL
                        col = g.COLOR_WHITE if flash else clr
                        game.fill_cell(BOARD_X, BOARD_Y, r, c, CELL, col)
                    else:
                        pt = board[r][c]
                        assert pt is not None
                        colors = PIECE_COLORS.get(pt)
                        if colors:
                            draw_block(game, BOARD_X + c * CELL, BOARD_Y + r * CELL, colors[0], colors[1], colors[2])
                        else:
                            game.fill_cell(BOARD_X, BOARD_Y, r, c, CELL, GARBAGE_COL)

        # ghost piece
        if not game_over and not clearing:
            gy = ghost_y()
            _m, _l, _d, ghost_col = PIECE_COLORS[current.type]
            for dx, dy in SHAPES[current.type][current.rot]:
                gx = BOARD_X + (current.x + dx) * CELL
                gyy = BOARD_Y + (gy + dy) * CELL
                game.fill_rect(gx + 1, gyy + 1, CELL - 2, CELL - 2, ghost_col)
                game.draw_rect(gx + 1, gyy + 1, CELL - 2, CELL - 2, g.COLOR_ARGB(80, 200, 200, 220))

        # current piece
        if not game_over and not clearing:
            for dx, dy in SHAPES[current.type][current.rot]:
                px = BOARD_X + (current.x + dx) * CELL
                py = BOARD_Y + (current.y + dy) * CELL
                draw_block(game, px, py, current.colors[0], current.colors[1], current.colors[2])

        # notification
        if notif_timer > 0 and notif_text:
            nx = BOARD_X + BOARD_W // 2 - len(notif_text) * 4
            ny = BOARD_Y + BOARD_H // 3
            game.fill_rect(nx - 4, ny - 2, len(notif_text) * 8 + 8, 14, g.COLOR_ARGB(180, 0, 0, 0))
            game.draw_text(nx, ny, notif_text, g.COLOR_YELLOW)

        # --- Sidebar ---
        sx = BOARD_X + BOARD_W + 15
        sy = BOARD_Y

        game.fill_rect(sx - 5, sy - 5, SIDEBAR, BOARD_H + 10, SIDEBAR_BG)
        game.draw_rect(sx - 5, sy - 5, SIDEBAR, BOARD_H + 10, BORDER)

        # title
        game.draw_text_scale(sx + 5, sy + 5, "TETRIS", ACCENT, 12, 12)

        # score
        yp = sy + 45
        game.draw_text(sx + 5, yp, "SCORE", DIM_TEXT)
        game.draw_printf(sx + 5, yp + 12, ACCENT, f"{score}")
        yp += 30
        game.draw_text(sx + 5, yp, "LEVEL", DIM_TEXT)
        game.draw_number(sx + 5, yp + 12, level, ACCENT)
        yp += 30
        game.draw_text(sx + 5, yp, "LINES", DIM_TEXT)
        game.draw_number(sx + 5, yp + 12, lines, ACCENT)

        # next piece
        yp += 35
        game.draw_text(sx + 5, yp, "NEXT", DIM_TEXT)
        game.fill_rect(sx + 5, yp + 12, SIDEBAR - 20, 48, BOARD_BG)
        game.draw_rect(sx + 5, yp + 12, SIDEBAR - 20, 48, BORDER)
        draw_mini_piece(game, next_piece.type, sx + 5 + (SIDEBAR - 20) // 2, yp + 36)

        # hold
        yp += 68
        game.draw_text(sx + 5, yp, "HOLD", DIM_TEXT)
        game.fill_rect(sx + 5, yp + 12, SIDEBAR - 20, 48, BOARD_BG)
        game.draw_rect(sx + 5, yp + 12, SIDEBAR - 20, 48, BORDER)
        if held is not None:
            draw_mini_piece(game, held.type, sx + 5 + (SIDEBAR - 20) // 2, yp + 36)  # pyright: ignore[reportUnreachable]

        # controls
        yp += 70
        game.draw_text(sx + 5, yp, "CONTROLS", ACCENT)
        yp += 16
        controls = [
            "<->  Move",
            "^    Rotate",
            "v    Soft drop",
            "SPC  Hard drop",
            "C    Hold",
            "P    Pause",
            "ESC  Quit",
        ]
        for line in controls:
            game.draw_text(sx + 5, yp, line, DIM_TEXT)
            yp += 13

        # FPS
        game.draw_printf(sx + 5, sy + BOARD_H - 10, g.COLOR_DARK_GRAY, f"FPS:{game.get_fps():.0f}")

        # --- Overlays ---
        if game_over:
            cx = BOARD_X + BOARD_W // 2
            cy = BOARD_Y + BOARD_H // 2
            game.fill_rect(cx - 80, cy - 35, 160, 70, g.COLOR_ARGB(200, 0, 0, 0))
            game.draw_rect(cx - 80, cy - 35, 160, 70, g.COLOR_RED)
            game.draw_text_scale(cx - 48, cy - 28, "GAME OVER", g.COLOR_RGB(255, 80, 80), 10, 10)
            game.draw_printf(cx - 50, cy + 0, TEXT_COL, f"Score: {score}")
            game.draw_text(cx - 45, cy + 18, "R to restart", g.COLOR_YELLOW)

        if paused and not game_over:
            cx = BOARD_X + BOARD_W // 2
            cy = BOARD_Y + BOARD_H // 2
            game.fill_rect(cx - 55, cy - 18, 110, 36, g.COLOR_ARGB(200, 0, 0, 0))
            game.draw_text_scale(cx - 30, cy - 12, "PAUSED", g.COLOR_YELLOW, 10, 10)

        game.update()
        game.wait_frame(FPS)


if __name__ == "__main__":
    main()
