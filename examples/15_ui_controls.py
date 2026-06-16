"""15_ui_controls.py - Enhanced UI Controls Demo

Demonstrates the immediate-mode UI helpers:
  button, checkbox, radio_box, toggle_button,
  slider, spinner, progress_bar, separator, label,
  text_input, dropdown, tab_bar, tooltip, v_separator,
  image_button, list_box, collapsible, color_picker,
  knob, menu.
Labels use the built-in 8x8 bitmap font, so keep them ASCII.

Controls:
  Mouse left button : interact with all UI controls
  Mouse wheel       : scroll in list_box
  Keyboard          : type in text input field
  ESC               : quit

Learn: button, checkbox, radio_box, toggle_button,
       slider, spinner, progress_bar, separator, label,
       text_input, dropdown, tab_bar, tooltip, v_separator,
       image_button, list_box, collapsible, color_picker,
       knob, menu, release-trigger UI, built-in 8x8 UI labels
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
    game.open(1100, 960, "15 - UI Controls", True)

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

    # --- Extended widget states ---
    player_name = "Player1"
    name_focused = False
    search_text = ""
    search_focused = False
    resolution_idx = 0
    resolution_open = False
    quality_idx = 1
    quality_open = False
    active_tab = 0

    # --- Advanced widget states ---
    list_items = [
        "APPLE",
        "BANANA",
        "CHERRY",
        "DATE",
        "ELDERBERRY",
        "FIG",
        "GRAPE",
        "HONEYDEW",
        "KIWI",
        "LEMON",
        "MANGO",
        "NECTARINE",
    ]
    list_idx = 0
    list_scroll = 0
    section_open = True
    section2_open = False
    knob_val = 50
    color_palette = [
        0xFF0000FF,
        0xFF00FF00,
        0xFFFF0000,
        0xFFFFFF00,
        0xFF00FFFF,
        0xFFFF00FF,
        0xFFFFFFFF,
        0xFF000000,
        0xFF800000,
        0xFF008000,
        0xFF000080,
        0xFF808000,
        0xFF800080,
        0xFF008080,
        0xFFC0C0C0,
        0xFF808080,
    ]
    color_idx = 0
    menu_open = False
    menu_result = -1
    menu_items = ["NEW GAME", "LOAD GAME", "OPTIONS", "CREDITS", "QUIT"]

    # create sprite for image_button demo
    icon_id = game.create_sprite(20, 20)
    for py in range(20):
        for px in range(20):
            c = g.COLOR_RGB(px * 12, py * 12, 200) if (px + py) % 2 == 0 else g.COLOR_RGB(40, 40, 60)
            game.set_sprite_pixel(icon_id, px, py, c)

    resolutions = ["640x480", "800x600", "1024x768", "1280x720", "1920x1080"]
    qualities = ["LOW", "MEDIUM", "HIGH", "ULTRA"]
    tab_names = ["GENERAL", "GRAPHICS", "AUDIO", "CONTROLS"]

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
        draw_panel(game, 804, 70, 276, 230, "Tabs & Tooltip")

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
            player_name = "Player1"
            search_text = ""
            resolution_idx = 0
            quality_idx = 1
            active_tab = 0
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

        # --- Tab Bar ---
        _, active_tab = game.tab_bar(814, 100, 256, tab_names, active_tab)

        # draw tab content area
        game.fill_rect(814, 126, 256, 96, g.COLOR_RGB(48, 58, 82))
        game.draw_rect(814, 126, 256, 96, g.COLOR_RGB(84, 94, 120))

        tab_contents = [
            "General settings",
            "Graphics options",
            "Audio settings",
            "Key bindings",
        ]
        game.draw_text(824, 136, tab_names[active_tab], g.COLOR_YELLOW)
        game.separator(824, 150, 236)
        game.draw_text(824, 158, tab_contents[active_tab], g.COLOR_LIGHT_GRAY)
        game.draw_text(824, 174, f"Tab {active_tab + 1}/{len(tab_names)}", g.COLOR_WHITE)

        # --- Tooltip ---
        game.separator(814, 198, 256)
        # hover button to show tooltip
        if game.button(824, 210, 100, 24, "HOVER ME", g.COLOR_RGB(100, 80, 160)):
            last_event = "HOVER BTN"
        mx = game.get_mouse_x()
        my = game.get_mouse_y()
        if g.GameLib.point_in_rect(mx, my, 824, 210, 100, 24):
            game.tooltip(mx + 12, my + 12, "Click to trigger!")

        if game.button(940, 210, 120, 24, "TIP BUTTON", g.COLOR_RGB(80, 120, 160)):
            last_event = "TIP BTN"
        if g.GameLib.point_in_rect(mx, my, 940, 210, 120, 24):
            game.tooltip(mx + 12, my + 12, "Another tooltip!")

        # =================================================================
        # ROW 2 - New controls (y=316 .. y=600)
        # =================================================================

        draw_panel(game, 20, 316, 260, 290, "Sliders")
        draw_panel(game, 296, 316, 260, 290, "Spinners")
        draw_panel(game, 572, 316, 260, 290, "Progress Bars")
        draw_panel(game, 848, 316, 232, 290, "Status")

        # --- VSeparator between slider groups ---
        game.v_separator(155, 354, 200)

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

        # =================================================================
        # ROW 3 - Extended controls (y=622 .. y=770)
        # =================================================================

        draw_panel(game, 20, 622, 350, 148, "Text Input")
        draw_panel(game, 386, 622, 350, 148, "Dropdown")

        # --- Text Input ---
        game.draw_text(40, 660, "NAME:", g.COLOR_WHITE)
        _, player_name, name_focused = game.text_input(90, 656, 200, player_name, name_focused)
        game.draw_text(40, 680, f"Hello, {player_name}!", g.COLOR_YELLOW)

        game.draw_text(40, 706, "SEARCH:", g.COLOR_WHITE)
        _, search_text, search_focused = game.text_input(100, 702, 190, search_text, search_focused)
        if search_text:
            game.draw_text(40, 722, f"Query: {search_text}", g.COLOR_LIGHT_GRAY)
        else:
            game.draw_text(40, 722, "Type to search...", g.COLOR_GRAY)

        game.separator(40, 740, 310)
        game.draw_text(40, 750, "Click field to focus,", g.COLOR_LIGHT_GRAY)
        game.draw_text(200, 750, "BACKSPACE to delete.", g.COLOR_LIGHT_GRAY)

        # --- Dropdown ---
        game.draw_text(406, 660, "RESOLUTION:", g.COLOR_WHITE)
        _, resolution_idx, resolution_open = game.dropdown(
            500,
            656,
            180,
            resolutions,
            resolution_idx,
            resolution_open,
        )

        game.draw_text(406, 700, "QUALITY:", g.COLOR_WHITE)
        _, quality_idx, quality_open = game.dropdown(
            500,
            696,
            180,
            qualities,
            quality_idx,
            quality_open,
        )

        game.separator(406, 734, 310)
        game.draw_text(406, 744, f"Selected: {resolutions[resolution_idx]}", g.COLOR_LIGHT_GRAY)
        game.draw_text(406, 758, f"Quality:  {qualities[quality_idx]}", g.COLOR_LIGHT_GRAY)

        # =================================================================
        # ROW 4 - Advanced controls (y=790 .. y=948)
        # =================================================================

        draw_panel(game, 20, 790, 240, 158, "ListBox")
        draw_panel(game, 276, 790, 200, 158, "Knob & Collapsible")
        draw_panel(game, 492, 790, 220, 158, "ColorPicker")
        draw_panel(game, 728, 790, 352, 158, "Menu & ImageButton")

        # --- ListBox ---
        _, list_idx, list_scroll = game.list_box(
            30,
            820,
            220,
            118,
            list_items,
            list_idx,
            list_scroll,
        )
        game.draw_text(30, 940, f"Selected: {list_items[list_idx]}", g.COLOR_YELLOW)

        # --- Knob ---
        _, knob_val = game.knob(290, 822, 50, knob_val, 0, 100)
        game.draw_text(350, 830, f"KNOB: {knob_val}", g.COLOR_WHITE)
        game.progress_bar(350, 846, 110, 12, knob_val, 100, g.COLOR_RGB(70, 130, 200))

        # --- Collapsible ---
        _, section_open = game.collapsible(286, 878, 180, "DETAILS", section_open)
        if section_open:
            game.fill_rect(286, 900, 180, 38, g.COLOR_RGB(40, 46, 62))
            game.draw_text(296, 908, "Expanded content", g.COLOR_LIGHT_GRAY)
            game.draw_text(296, 922, "inside section", g.COLOR_LIGHT_GRAY)

        _, section2_open = game.collapsible(286, 940 if not section_open else 940, 180, "EXTRA", section2_open)

        # --- ColorPicker ---
        _, color_idx = game.color_picker(502, 822, color_palette, color_idx)
        selected_color = color_palette[color_idx]
        game.fill_rect(502, 886, 200, 20, selected_color)
        game.draw_rect(502, 886, 200, 20, g.COLOR_RGB(84, 94, 120))
        r_val = g.COLOR_GET_R(selected_color)
        g_val = g.COLOR_GET_G(selected_color)
        b_val = g.COLOR_GET_B(selected_color)
        game.draw_text(502, 912, f"R:{r_val} G:{g_val} B:{b_val}", g.COLOR_LIGHT_GRAY)
        game.draw_text(502, 928, f"Selected: #{selected_color:08X}", g.COLOR_LIGHT_GRAY)

        # --- Menu ---
        if game.button(738, 822, 120, 24, "OPEN MENU", g.COLOR_RGB(80, 120, 160)):
            menu_open = True
        menu_result_idx, menu_open = game.menu(738, 852, menu_items, menu_open)
        if menu_result_idx >= 0:
            menu_result = menu_result_idx
            last_event = f"MENU: {menu_items[menu_result]}"
        game.draw_text(870, 826, "Last pick:", g.COLOR_WHITE)
        if menu_result >= 0:
            game.draw_text(870, 842, menu_items[menu_result], g.COLOR_YELLOW)

        # --- ImageButton ---
        if game.image_button(738, 880, 56, 56, icon_id, g.COLOR_RGB(60, 70, 100)):
            last_event = "IMAGE BTN"
        game.draw_text(804, 896, "ImageButton", g.COLOR_WHITE)
        game.draw_text(804, 912, "with sprite", g.COLOR_LIGHT_GRAY)

        game.update()
        game.wait_frame(60)


if __name__ == "__main__":
    main()
