"""01_hello.py - Hello World

The simplest GameLib program: create a window and display text.
Learn: open, clear, draw_text, draw_text_scale, update, wait_frame, is_closed
"""
import pyezgame as g


def main() -> None:
    game = g.GameLib()
    game.open(640, 480, "01 - Hello World", True)

    while not game.is_closed():
        game.clear(g.COLOR_DARK_BLUE)

        # Large title
        game.draw_text_scale(160, 180, "Hello, GameLib!", g.COLOR_GOLD, 24, 24)

        # Normal text
        game.draw_text(230, 240, "Welcome to GameLib!", g.COLOR_WHITE)
        game.draw_text(210, 270, "Press ESC to exit, or close", g.COLOR_GRAY)
        game.draw_text(210, 280, "the window to quit.", g.COLOR_GRAY)

        # Show running time
        game.draw_printf(10, 460, g.COLOR_LIGHT_GRAY, f"Time: {game.get_time():.1f} s")

        if game.is_key_pressed(g.KEY_ESCAPE):
            break

        game.update()
        game.wait_frame(60)


if __name__ == "__main__":
    main()
