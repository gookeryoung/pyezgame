"""15_ui_controls.py - Basic UI Controls Demo

Demonstrates the immediate-mode button, checkbox, radio_box
and toggle_button helpers.
Labels use the built-in 8x8 bitmap font, so keep them ASCII.

Controls:
  Mouse left button : interact with buttons and checkboxes
  ESC               : quit

Learn: button, checkbox, radio_box, toggle_button,
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
    game.open(960, 520, "15 - UI Controls", True)

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

    while not game.is_closed():
        if game.is_key_pressed(g.KEY_ESCAPE):
            break

        draw_backdrop(game, show_grid)

        game.fill_rect(0, 0, 960, 56, g.COLOR_RGB(10, 14, 24))
        game.draw_text_scale(20, 14, "UI CONTROLS", g.COLOR_WHITE, 16, 16)
        game.draw_text(20, 40, "Mouse: press inside, release inside to trigger. ESC quits.", g.COLOR_LIGHT_GRAY)

        draw_panel(game, 20, 76, 184, 420, "Buttons")
        draw_panel(game, 224, 76, 184, 420, "Checkboxes")
        draw_panel(game, 428, 76, 184, 420, "RadioBox")
        draw_panel(game, 632, 76, 184, 420, "Toggle")
        draw_panel(game, 836, 76, 104, 420, "Status")

        if game.button(40, 116, 144, 32, "START", g.COLOR_RGB(52, 150, 92)):
            start_count += 1
            last_event = "START"
        if game.button(40, 160, 144, 32, "RESET", g.COLOR_RGB(196, 142, 46)):
            music_on = True
            sfx_on = True
            show_grid = False
            hard_mode = False
            reset_count += 1
            last_event = "RESET"
        if game.button(40, 204, 144, 32, "QUIT", g.COLOR_RGB(180, 76, 76)):
            break

        game.draw_text(40, 264, "The button label uses", g.COLOR_LIGHT_GRAY)
        game.draw_text(40, 280, "the built-in 8x8 font.", g.COLOR_LIGHT_GRAY)
        game.draw_text(40, 320, "Visual states:", g.COLOR_WHITE)
        game.draw_text(40, 340, "NORMAL / HOVER / PRESSED", g.COLOR_LIGHT_GRAY)

        triggered, music_on = game.checkbox(244, 116, "MUSIC", music_on)
        if triggered:
            last_event = "MUSIC ON" if music_on else "MUSIC OFF"
        triggered, sfx_on = game.checkbox(244, 152, "SFX", sfx_on)
        if triggered:
            last_event = "SFX ON" if sfx_on else "SFX OFF"
        triggered, show_grid = game.checkbox(244, 188, "SHOW GRID", show_grid)
        if triggered:
            last_event = "GRID ON" if show_grid else "GRID OFF"
        triggered, hard_mode = game.checkbox(244, 224, "HARD MODE", hard_mode)
        if triggered:
            last_event = "HARD ON" if hard_mode else "HARD OFF"

        game.draw_text(244, 276, "Click covers box", g.COLOR_WHITE)
        game.draw_text(244, 292, "and label.", g.COLOR_LIGHT_GRAY)
        game.draw_text(244, 324, "4 states:", g.COLOR_WHITE)
        game.draw_text(244, 340, "CHK/UNCHK", g.COLOR_LIGHT_GRAY)
        game.draw_text(244, 356, "+ hover.", g.COLOR_LIGHT_GRAY)

        triggered, difficulty = game.radio_box(448, 116, "EASY", difficulty, 0)
        if triggered:
            last_event = "EASY"
        triggered, difficulty = game.radio_box(448, 152, "MEDIUM", difficulty, 1)
        if triggered:
            last_event = "MEDIUM"
        triggered, difficulty = game.radio_box(448, 188, "HARD", difficulty, 2)
        if triggered:
            last_event = "HARD"

        diff_names = ["EASY", "MEDIUM", "HARD"]

        game.draw_text(448, 232, "Same group shares", g.COLOR_WHITE)
        game.draw_text(448, 248, "one int value.", g.COLOR_LIGHT_GRAY)
        game.draw_text(448, 280, "Selected:", g.COLOR_WHITE)
        game.draw_text(448, 296, diff_names[difficulty], g.COLOR_YELLOW)
        game.draw_text(448, 336, "Circle + dot", g.COLOR_WHITE)
        game.draw_text(448, 352, "instead of box.", g.COLOR_LIGHT_GRAY)

        triggered, paused = game.toggle_button(652, 116, 144, 32, "PAUSE", paused,
                                                g.COLOR_RGB(180, 76, 76))
        if triggered:
            last_event = "PAUSED" if paused else "RESUME"
        triggered, turbo = game.toggle_button(652, 160, 144, 32, "TURBO", turbo,
                                               g.COLOR_RGB(52, 150, 92))
        if triggered:
            last_event = "TURBO ON" if turbo else "TURBO OFF"

        game.draw_text(652, 216, "Toggled=ON shows", g.COLOR_WHITE)
        game.draw_text(652, 232, "sunken bevel.", g.COLOR_LIGHT_GRAY)
        game.draw_text(652, 264, "PAUSED:", g.COLOR_WHITE)
        game.draw_text(652, 280, "YES" if paused else "NO",
                        g.COLOR_YELLOW if paused else g.COLOR_LIGHT_GRAY)
        game.draw_text(652, 312, "TURBO:", g.COLOR_WHITE)
        game.draw_text(652, 328, "YES" if turbo else "NO",
                        g.COLOR_YELLOW if turbo else g.COLOR_LIGHT_GRAY)

        game.draw_text(856, 116, "LAST EVENT", g.COLOR_WHITE)
        game.draw_text(856, 136, last_event, g.COLOR_YELLOW)
        game.draw_text(856, 176, "COUNTS", g.COLOR_WHITE)
        game.draw_printf(856, 196, g.COLOR_LIGHT_GRAY, f"START: {start_count}")
        game.draw_printf(856, 212, g.COLOR_LIGHT_GRAY, f"RESET: {reset_count}")

        game.draw_text(856, 252, "FLAGS", g.COLOR_WHITE)
        game.draw_printf(856, 272, g.COLOR_LIGHT_GRAY, f"MUSIC: {'ON' if music_on else 'OFF'}")
        game.draw_printf(856, 288, g.COLOR_LIGHT_GRAY, f"SFX: {'ON' if sfx_on else 'OFF'}")
        game.draw_printf(856, 304, g.COLOR_LIGHT_GRAY, f"GRID: {'ON' if show_grid else 'OFF'}")
        game.draw_printf(856, 320, g.COLOR_LIGHT_GRAY, f"HARD: {'ON' if hard_mode else 'OFF'}")

        game.draw_text(856, 352, "DIFF:", g.COLOR_WHITE)
        game.draw_text(856, 368, diff_names[difficulty], g.COLOR_YELLOW)
        game.draw_printf(856, 384, g.COLOR_LIGHT_GRAY, f"PAUSE:{'Y' if paused else 'N'}")
        game.draw_printf(856, 400, g.COLOR_LIGHT_GRAY, f"TURBO:{'Y' if turbo else 'N'}")

        game.update()
        game.wait_frame(60)


if __name__ == "__main__":
    main()
