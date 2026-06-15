"""15_ui_controls.py - Enhanced UI Controls Demo

Demonstrates the immediate-mode UI helpers:
  button, checkbox, radio_box, toggle_button,
  slider, spinner, progress_bar, separator, label.
Labels use the built-in 8x8 bitmap font, so keep them ASCII.

Controls:
  Mouse left button : interact with all UI controls
  ESC               : quit

Learn: button, checkbox, radio_box, toggle_button,
       slider, spinner, progress_bar, separator, label,
       release-trigger UI, built-in 8x8 UI labels
"""

import pyezgame as g


def draw_panel(game: g.GameLib, x: int, y: int, w: int, h: int, title: str) -> None:
    game.fill_rect(x, y, w, h, g.COLOR_RGB(28, 34, 50))
    game.draw_rect(x, y, w, h, g.COLOR_RGB(84, 94, 120))
    game.fill_rect(x + 1, y + 1, w - 2, 22, g.COLOR_RGB(38, 48, 72))
    game.draw_text(x + 8, y + 7, title, g.COLOR_WHITE)


def draw_backdrop(game: g.GameLib, show_grid: bool) -> None:
    game.clear(g.COLOR_RGB(18, 22, 34))

    for y in range(0, game.get_height(), 40):
        stripe = g.COLOR_RGB(20, 26, 40) if ((y // 40) & 1) else g.COLOR_RGB(16, 20, 32)
        game.fill_rect(0, y, game.get_width(), 40, stripe)

    if not show_grid:
        return

    grid_color = g.COLOR_ARGB(70, 120, 138, 168)
    for x in range(0, game.get_width(), 20):
        game.draw_line(x, 0, x, game.get_height() - 1, grid_color)
    for y in range(0, game.get_height(), 20):
        game.draw_line(0, y, game.get_width() - 1, y, grid_color)


def main() -> None:
    game = g.GameLib()
    game.open(1100, 620, "15 - UI Controls", True)

    # --- State variables ---
    music_on = True
    sfx_on = True
    show_grid = False
    hard_mode = False
    difficulty = 0
    paused = False
    turbo = False
    start_count = 0
    reset_count = 0
    last_event = "NONE"

    # --- New widget states ---
    volume = 75
    brightness = 50
    speed = 30
    hp = 100
    level = 1
    score_mult = 1

    while not game.is_closed():
        if game.is_key_pressed(g.KEY_ESCAPE):
            break

        draw_backdrop(game, show_grid)

        # === Top bar ===
        game.fill_rect(0, 0, 1100, 56, g.COLOR_RGB(10, 14, 24))
        game.draw_text_scale(20, 14, "UI CONTROLS", g.COLOR_WHITE, 16, 16)
        game.draw_text(20, 40, "Mouse: press/release inside to trigger. ESC quits.", g.COLOR_LIGHT_GRAY)

        # =================================================================
        # ROW 1 - Original controls (y=70 .. y=296)
        # =================================================================

        draw_panel(game, 20, 70, 180, 230, "Buttons")
        draw_panel(game, 216, 70, 180, 230, "Checkboxes")
        draw_panel(game, 412, 70, 180, 230, "RadioBox")
        draw_panel(game, 608, 70, 180, 230, "Toggle")

        # --- Buttons ---
        if game.button(40, 108, 140, 28, "START", g.COLOR_RGB(52, 150, 92)):
            start_count += 1
            last_event = "START"
        if game.button(40, 148, 140, 28, "RESET", g.COLOR_RGB(196, 142, 46)):
            music_on = True
            sfx_on = True
            show_grid = False
            hard_mode = False
            volume = 75
            brightness = 50
            speed = 30
            hp = 100
            level = 1
            score_mult = 1
            reset_count += 1
            last_event = "RESET"
        if game.button(40, 188, 140, 28, "QUIT", g.COLOR_RGB(180, 76, 76)):
            break

        game.separator(40, 228, 140)
        game.draw_text(40, 240, "States: NORMAL", g.COLOR_LIGHT_GRAY)
        game.draw_text(40, 256, " HOVER / PRESSED", g.COLOR_LIGHT_GRAY)

        # --- Checkboxes ---
        triggered, music_on = game.checkbox(236, 108, "MUSIC", music_on)
        if triggered:
            last_event = "MUSIC ON" if music_on else "MUSIC OFF"
        triggered, sfx_on = game.checkbox(236, 140, "SFX", sfx_on)
        if triggered:
            last_event = "SFX ON" if sfx_on else "SFX OFF"
        triggered, show_grid = game.checkbox(236, 172, "SHOW GRID", show_grid)
        if triggered:
            last_event = "GRID ON" if show_grid else "GRID OFF"
        triggered, hard_mode = game.checkbox(236, 204, "HARD MODE", hard_mode)
        if triggered:
            last_event = "HARD ON" if hard_mode else "HARD OFF"

        game.separator(236, 236, 140)
        game.draw_text(236, 248, "Click toggles the", g.COLOR_LIGHT_GRAY)
        game.draw_text(236, 264, "checkbox on/off.", g.COLOR_LIGHT_GRAY)

        # --- RadioBox ---
        triggered, difficulty = game.radio_box(432, 108, "EASY", difficulty, 0)
        if triggered:
            last_event = "EASY"
        triggered, difficulty = game.radio_box(432, 140, "MEDIUM", difficulty, 1)
        if triggered:
            last_event = "MEDIUM"
        triggered, difficulty = game.radio_box(432, 172, "HARD", difficulty, 2)
        if triggered:
            last_event = "HARD"

        diff_names = ["EASY", "MEDIUM", "HARD"]

        game.separator(432, 208, 140)
        game.draw_text(432, 220, "Selected:", g.COLOR_WHITE)
        game.draw_text(432, 236, diff_names[difficulty], g.COLOR_YELLOW)
        game.draw_text(432, 260, "Group shares one", g.COLOR_LIGHT_GRAY)
        game.draw_text(432, 276, "int value.", g.COLOR_LIGHT_GRAY)

        # --- Toggle ---
        triggered, paused = game.toggle_button(628, 108, 140, 28, "PAUSE", paused, g.COLOR_RGB(180, 76, 76))
        if triggered:
            last_event = "PAUSED" if paused else "RESUME"
        triggered, turbo = game.toggle_button(628, 148, 140, 28, "TURBO", turbo, g.COLOR_RGB(52, 150, 92))
        if triggered:
            last_event = "TURBO ON" if turbo else "TURBO OFF"

        game.separator(628, 188, 140)
        game.draw_text(628, 200, "Toggled=ON shows", g.COLOR_WHITE)
        game.draw_text(628, 216, "sunken bevel.", g.COLOR_LIGHT_GRAY)
        game.draw_text(628, 244, "PAUSED:", g.COLOR_WHITE)
        game.draw_text(628, 260, "YES" if paused else "NO", g.COLOR_YELLOW if paused else g.COLOR_LIGHT_GRAY)

        # =================================================================
        # ROW 2 - New controls (y=316 .. y=600)
        # =================================================================

        draw_panel(game, 20, 316, 260, 290, "Sliders")
        draw_panel(game, 296, 316, 260, 290, "Spinners")
        draw_panel(game, 572, 316, 260, 290, "Progress Bars")
        draw_panel(game, 848, 316, 232, 290, "Status")

        # --- Sliders ---
        game.draw_text(40, 354, "VOLUME:", g.COLOR_WHITE)
        game.draw_printf(160, 354, g.COLOR_YELLOW, f"{volume}")
        _, volume = game.slider(40, 370, 220, volume, 0, 100)

        game.draw_text(40, 402, "BRIGHTNESS:", g.COLOR_WHITE)
        game.draw_printf(160, 402, g.COLOR_YELLOW, f"{brightness}")
        _, brightness = game.slider(40, 418, 220, brightness, 0, 100)

        game.draw_text(40, 450, "SPEED:", g.COLOR_WHITE)
        game.draw_printf(160, 450, g.COLOR_YELLOW, f"{speed}")
        _, speed = game.slider(40, 466, 220, speed, 0, 100)

        game.separator(40, 498, 220)
        game.draw_text(40, 510, "Drag the handle to", g.COLOR_LIGHT_GRAY)
        game.draw_text(40, 526, "adjust the value.", g.COLOR_LIGHT_GRAY)
        game.draw_text(40, 556, "Range: 0 ~ 100", g.COLOR_LIGHT_GRAY)

        # --- Spinners ---
        game.draw_text(316, 354, "HP:", g.COLOR_WHITE)
        _, hp = game.spinner(370, 350, 120, hp, 0, 999, 10)

        game.draw_text(316, 402, "LEVEL:", g.COLOR_WHITE)
        _, level = game.spinner(370, 398, 120, level, 1, 99, 1)

        game.draw_text(316, 450, "SCORE MULT:", g.COLOR_WHITE)
        _, score_mult = game.spinner(420, 446, 70, score_mult, 1, 10, 1)

        game.separator(316, 498, 220)
        game.draw_text(316, 510, "Click -/+ buttons", g.COLOR_LIGHT_GRAY)
        game.draw_text(316, 526, "to change value.", g.COLOR_LIGHT_GRAY)
        game.draw_text(316, 556, "Step is configurable.", g.COLOR_LIGHT_GRAY)

        # --- Progress Bars ---
        game.draw_text(592, 354, "VOLUME BAR:", g.COLOR_WHITE)
        game.progress_bar(592, 370, 220, 18, volume, 100, g.COLOR_RGB(52, 150, 92))

        game.draw_text(592, 402, "BRIGHTNESS BAR:", g.COLOR_WHITE)
        game.progress_bar(592, 418, 220, 18, brightness, 100, g.COLOR_RGB(70, 130, 200))

        game.draw_text(592, 450, "LOADING BAR:", g.COLOR_WHITE)
        game.progress_bar(592, 466, 220, 18, speed, 100, g.COLOR_RGB(196, 142, 46))

        game.separator(592, 498, 220)
        game.draw_text(592, 510, "Bars are driven by", g.COLOR_LIGHT_GRAY)
        game.draw_text(592, 526, "slider values above.", g.COLOR_LIGHT_GRAY)

        # HP progress bar
        game.draw_text(592, 554, "HP:", g.COLOR_WHITE)
        hp_color = g.COLOR_RGB(52, 180, 92) if hp > 50 else g.COLOR_RGB(200, 76, 76)
        game.progress_bar(620, 550, 192, 18, hp, 999, hp_color)

        # --- Status panel ---
        # Labels at the top of status panel
        game.label(858, 350, 212, 20, "LAST EVENT", g.COLOR_RGB(38, 48, 72), g.COLOR_WHITE)
        game.label(858, 376, 212, 20, last_event, g.COLOR_RGB(52, 60, 82), g.COLOR_YELLOW)

        game.draw_text(858, 410, "COUNTS", g.COLOR_WHITE)
        game.draw_printf(858, 426, g.COLOR_LIGHT_GRAY, f"START: {start_count}")
        game.draw_printf(858, 442, g.COLOR_LIGHT_GRAY, f"RESET: {reset_count}")

        game.separator(858, 462, 212)

        game.draw_text(858, 474, "FLAGS", g.COLOR_WHITE)
        game.draw_printf(858, 490, g.COLOR_LIGHT_GRAY, f"MUSIC:{'ON' if music_on else 'OFF'}")
        game.draw_printf(858, 506, g.COLOR_LIGHT_GRAY, f"SFX:  {'ON' if sfx_on else 'OFF'}")
        game.draw_printf(858, 522, g.COLOR_LIGHT_GRAY, f"GRID: {'ON' if show_grid else 'OFF'}")
        game.draw_printf(858, 538, g.COLOR_LIGHT_GRAY, f"HARD: {'ON' if hard_mode else 'OFF'}")

        game.draw_printf(858, 558, g.COLOR_LIGHT_GRAY, f"DIFF:{diff_names[difficulty]}")
        game.draw_printf(858, 574, g.COLOR_LIGHT_GRAY, f"PAUSE:{'Y' if paused else 'N'} TURBO:{'Y' if turbo else 'N'}")

        game.update()
        game.wait_frame(60)


if __name__ == "__main__":
    main()
