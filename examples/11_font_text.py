"""11_font_text.py - Font Text and UI Demo

Demonstrates draw_text_font, draw_printf_font, text measurement,
show_mouse, and show_message.
Learn: draw_text_font, draw_printf_font, get_text_width_font, show_mouse, show_message
"""

import pyezgame as g

FONT_MONO = "Consolas"
FONT_CJK = "MS Gothic"


def main() -> None:
    game = g.GameLib()
    game.open(720, 520, "11 - Font Text and UI", True)
    game.show_fps(True)

    mouse_visible = True
    last_message_result = g.MESSAGEBOX_RESULT_OK

    while not game.is_closed():
        time_sec = game.get_time()
        score = int(time_sec * 123.0)
        title_w = game.get_text_width_font("DrawTextFont + DrawPrintfFont", 30)

        if last_message_result == g.MESSAGEBOX_RESULT_YES:
            result_text = "YES"
        elif last_message_result == g.MESSAGEBOX_RESULT_NO:
            result_text = "NO"
        else:
            result_text = "OK"

        if game.is_key_pressed(g.KEY_H):
            mouse_visible = not mouse_visible
            game.show_mouse(mouse_visible)
        if game.is_key_pressed(g.KEY_M):
            last_message_result = game.show_message(
                "GameLib now has DrawPrintfFont, ShowMouse and ShowMessage.", "New UI APIs", g.MESSAGEBOX_OK
            )
        if game.is_key_pressed(g.KEY_Y):
            last_message_result = game.show_message("Show the mouse cursor?", "ShowMessage YES/NO", g.MESSAGEBOX_YESNO)
            mouse_visible = last_message_result != g.MESSAGEBOX_RESULT_NO
            game.show_mouse(mouse_visible)
        if game.is_key_pressed(g.KEY_ESCAPE):
            break

        game.clear(g.COLOR_RGB(18, 24, 34))

        game.fill_rect(18, 18, 684, 70, g.COLOR_ARGB(215, 34, 42, 56))
        game.draw_rect(18, 18, 684, 70, g.COLOR_LIGHT_GRAY)
        game.draw_text_font((game.get_width() - title_w) // 2, 32, "DrawTextFont + DrawPrintfFont", g.COLOR_WHITE, 30)
        game.draw_text(30, 74, "Built-in text below is ASCII only. Font text can use Unicode.", g.COLOR_LIGHT_GRAY)

        game.fill_rect(18, 104, 420, 214, g.COLOR_ARGB(205, 26, 34, 46))
        game.draw_rect(18, 104, 420, 214, g.COLOR_LIGHT_GRAY)
        game.draw_text(28, 114, "Scalable font text", g.COLOR_WHITE)
        game.draw_text_font(28, 142, "Scalable font - supports Unicode", g.COLOR_YELLOW, 24)
        game.draw_text_font(28, 178, "CJK font rendering test", g.COLOR_CYAN, FONT_CJK, 22)
        game.draw_text_font(28, 214, "Different sizes: 18 / 24 / 32", g.COLOR_GREEN, 18)
        game.draw_text_font(28, 240, "Different sizes: 18 / 24 / 32", g.COLOR_GREEN, 24)
        game.draw_text_font(28, 274, "Different sizes: 18 / 24 / 32", g.COLOR_GREEN, 32)

        game.fill_rect(456, 104, 246, 214, g.COLOR_ARGB(205, 34, 42, 56))
        game.draw_rect(456, 104, 246, 214, g.COLOR_LIGHT_GRAY)
        game.draw_text(466, 114, "DrawPrintfFont", g.COLOR_WHITE)
        game.draw_printf_font(470, 146, g.COLOR_GOLD, 24, f"Score: {score:05d}")
        game.draw_printf_font(470, 180, g.COLOR_SKY_BLUE, FONT_MONO, 18, f"Time: {time_sec:5.1f} s")
        game.draw_printf_font(470, 206, g.COLOR_WHITE, FONT_MONO, 18, f"FPS: {game.get_fps():5.1f}")
        game.draw_printf_font(
            470, 232, g.COLOR_PINK, FONT_MONO, 18, f"Mouse: {game.get_mouse_x():3d}, {game.get_mouse_y():3d}"
        )
        cursor_str = "visible" if mouse_visible else "hidden"
        game.draw_printf_font(470, 258, g.COLOR_LIGHT_GRAY, FONT_MONO, 18, f"Cursor: {cursor_str}")
        game.draw_printf_font(470, 284, g.COLOR_LIGHT_GRAY, FONT_MONO, 18, f"Last dialog: {result_text}")

        game.fill_rect(18, 338, 684, 136, g.COLOR_ARGB(205, 28, 36, 48))
        game.draw_rect(18, 338, 684, 136, g.COLOR_LIGHT_GRAY)
        game.draw_text(28, 348, "Interactive UI helpers", g.COLOR_WHITE)
        game.draw_text_font(28, 376, "H: Toggle mouse  M: Show OK dialog", g.COLOR_CYAN, 22)
        game.draw_text_font(28, 408, "Y: Show YES/NO dialog and sync mouse state", g.COLOR_CYAN, 22)
        game.draw_text_font(28, 440, "ESC: Quit", g.COLOR_GRAY, 18)

        game.draw_text_font(28, 480, "中文字体示例.", g.COLOR_LIGHT_GRAY, 18)
        game.draw_text_font(128, 480, "中文字体示例.", g.COLOR_LIGHT_GRAY, 18)
        game.draw_text_font(228, 480, "中文字体示例.", g.COLOR_LIGHT_GRAY, 18)

        game.update()
        game.wait_frame(60)


if __name__ == "__main__":
    main()
