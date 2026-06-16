"""15_ui_controls.py - Tabbed UI Controls Demo

Demonstrates ALL immediate-mode UI helpers organized in tab pages:
  Tab 1 BASIC    : button, checkbox, radio_box, toggle_button, separator, label
  Tab 2 VALUES   : slider, spinner, progress_bar, knob, v_separator
  Tab 3 INPUT    : text_input, dropdown, tab_bar, tooltip
  Tab 4 ADVANCED : list_box, color_picker, collapsible, image_button, menu
  Tab 5 STATUS   : status dashboard (last event, counts, flags)

Controls:
  Mouse left button : interact with all UI controls
  Mouse wheel       : scroll in list_box
  Keyboard          : type in text input field
  ESC               : quit

Learn: tab_panel, button, checkbox, radio_box, toggle_button,
       slider, spinner, progress_bar, separator, label,
       text_input, dropdown, tab_bar, tooltip, v_separator,
       image_button, list_box, collapsible, color_picker,
       knob, menu
"""

from __future__ import annotations

from typing import Any

import pyezgame as g

WIN_W, WIN_H = 800, 620


def draw_panel(game: g.GameLib, x: int, y: int, w: int, h: int, title: str) -> None:
    game.fill_rect(x, y, w, h, g.COLOR_RGB(28, 34, 50))
    game.draw_rect(x, y, w, h, g.COLOR_RGB(84, 94, 120))
    game.fill_rect(x + 1, y + 1, w - 2, 20, g.COLOR_RGB(38, 48, 72))
    game.draw_text(x + 6, y + 6, title, g.COLOR_WHITE)


def draw_backdrop(game: g.GameLib) -> None:
    game.clear(g.COLOR_RGB(18, 22, 34))
    for y in range(0, game.get_height(), 40):
        stripe = g.COLOR_RGB(20, 26, 40) if ((y // 40) & 1) else g.COLOR_RGB(16, 20, 32)
        game.fill_rect(0, y, game.get_width(), 40, stripe)


# ----- Tab content drawing functions -----


def draw_basic_tab(game: g.GameLib, cx: int, cy: int, state: dict[str, Any]) -> None:
    pw = 170
    gap = 8
    px = cx + 4

    draw_panel(game, px, cy, pw, 280, "Buttons")
    draw_panel(game, px + pw + gap, cy, pw, 280, "Checkboxes")
    draw_panel(game, px + 2 * (pw + gap), cy, pw, 280, "RadioBox")
    draw_panel(game, px + 3 * (pw + gap), cy, pw, 280, "Toggle & Label")

    # Buttons
    bx, by = px + 10, cy + 28
    if game.button(bx, by, 148, 26, "START", g.COLOR_RGB(52, 150, 92)):
        state["start_count"] += 1
        state["last_event"] = "START"
    if game.button(bx, by + 36, 148, 26, "RESET", g.COLOR_RGB(196, 142, 46)):
        _reset_all(state)
    if game.button(bx, by + 72, 148, 26, "QUIT", g.COLOR_RGB(180, 76, 76)):
        state["quit"] = True
    game.separator(bx, by + 110, 148)
    game.draw_text(bx, by + 120, "States: NORMAL", g.COLOR_LIGHT_GRAY)
    game.draw_text(bx, by + 134, " HOVER / PRESSED", g.COLOR_LIGHT_GRAY)

    # Checkboxes
    bx2 = px + pw + gap + 10
    _, state["music_on"] = game.checkbox(bx2, by, "MUSIC", state["music_on"])
    _, state["sfx_on"] = game.checkbox(bx2, by + 28, "SFX", state["sfx_on"])
    _, state["show_grid"] = game.checkbox(bx2, by + 56, "SHOW GRID", state["show_grid"])
    _, state["hard_mode"] = game.checkbox(bx2, by + 84, "HARD MODE", state["hard_mode"])
    game.separator(bx2, by + 120, 148)
    game.draw_text(bx2, by + 130, "Click toggles", g.COLOR_LIGHT_GRAY)
    game.draw_text(bx2, by + 144, "checkbox on/off.", g.COLOR_LIGHT_GRAY)

    # RadioBox
    bx3 = px + 2 * (pw + gap) + 10
    _, state["difficulty"] = game.radio_box(bx3, by, "EASY", state["difficulty"], 0)
    _, state["difficulty"] = game.radio_box(bx3, by + 28, "MEDIUM", state["difficulty"], 1)
    _, state["difficulty"] = game.radio_box(bx3, by + 56, "HARD", state["difficulty"], 2)
    game.separator(bx3, by + 96, 148)
    diff_names = ["EASY", "MEDIUM", "HARD"]
    game.draw_text(bx3, by + 108, "Selected:", g.COLOR_WHITE)
    game.draw_text(bx3, by + 122, diff_names[state["difficulty"]], g.COLOR_YELLOW)
    game.draw_text(bx3, by + 146, "Group shares one", g.COLOR_LIGHT_GRAY)
    game.draw_text(bx3, by + 160, "int value.", g.COLOR_LIGHT_GRAY)

    # Toggle & Label
    bx4 = px + 3 * (pw + gap) + 10
    _, state["paused"] = game.toggle_button(bx4, by, 148, 26, "PAUSE", state["paused"], g.COLOR_RGB(180, 76, 76))
    _, state["turbo"] = game.toggle_button(bx4, by + 36, 148, 26, "TURBO", state["turbo"], g.COLOR_RGB(52, 150, 92))
    game.separator(bx4, by + 76, 148)
    game.draw_text(bx4, by + 86, "PAUSED:", g.COLOR_WHITE)
    game.draw_text(
        bx4,
        by + 100,
        "YES" if state["paused"] else "NO",
        g.COLOR_YELLOW if state["paused"] else g.COLOR_LIGHT_GRAY,
    )
    game.label(bx4, by + 130, 148, 20, "LABEL WIDGET", g.COLOR_RGB(70, 50, 120), g.COLOR_WHITE)
    game.label(bx4, by + 158, 148, 20, "WITH BG COLOR", g.COLOR_RGB(50, 100, 70), g.COLOR_WHITE)


def draw_values_tab(game: g.GameLib, cx: int, cy: int, state: dict[str, Any]) -> None:
    pw = 240
    gap = 8
    px = cx + 4

    draw_panel(game, px, cy, pw, 280, "Sliders")
    draw_panel(game, px + pw + gap, cy, pw, 280, "Spinners & Knob")
    draw_panel(game, px + 2 * (pw + gap), cy, pw + 50, 280, "Progress Bars")

    # Sliders
    sx, sy = px + 10, cy + 30
    game.draw_text(sx, sy, "VOLUME:", g.COLOR_WHITE)
    game.draw_printf(sx + 100, sy, g.COLOR_YELLOW, f"{state['volume']}")
    _, state["volume"] = game.slider(sx, sy + 14, 218, state["volume"], 0, 100)

    game.draw_text(sx, sy + 50, "BRIGHTNESS:", g.COLOR_WHITE)
    game.draw_printf(sx + 100, sy + 50, g.COLOR_YELLOW, f"{state['brightness']}")
    _, state["brightness"] = game.slider(sx, sy + 64, 218, state["brightness"], 0, 100)

    game.draw_text(sx, sy + 100, "SPEED:", g.COLOR_WHITE)
    game.draw_printf(sx + 100, sy + 100, g.COLOR_YELLOW, f"{state['speed']}")
    _, state["speed"] = game.slider(sx, sy + 114, 218, state["speed"], 0, 100)

    game.separator(sx, sy + 150, 218)
    game.draw_text(sx, sy + 162, "Drag the handle", g.COLOR_LIGHT_GRAY)
    game.draw_text(sx, sy + 176, "to adjust value.", g.COLOR_LIGHT_GRAY)

    # Spinners & Knob
    sx2 = px + pw + gap + 10
    game.draw_text(sx2, sy, "HP:", g.COLOR_WHITE)
    _, state["hp"] = game.spinner(sx2 + 80, sy - 4, 120, state["hp"], 0, 999, 10)

    game.draw_text(sx2, sy + 44, "LEVEL:", g.COLOR_WHITE)
    _, state["level"] = game.spinner(sx2 + 80, sy + 40, 120, state["level"], 1, 99, 1)

    game.draw_text(sx2, sy + 88, "MULT:", g.COLOR_WHITE)
    _, state["score_mult"] = game.spinner(sx2 + 80, sy + 84, 120, state["score_mult"], 1, 10, 1)

    game.v_separator(sx2 + 110, sy + 124, 120)

    # Knob
    game.draw_text(sx2 + 130, sy, "KNOB:", g.COLOR_WHITE)
    game.draw_printf(sx2 + 180, sy, g.COLOR_YELLOW, f"{state['knob_val']}")
    _, state["knob_val"] = game.knob(sx2 + 140, sy + 20, 56, state["knob_val"], 0, 100)
    game.progress_bar(sx2 + 130, sy + 84, 80, 12, state["knob_val"], 100, g.COLOR_RGB(70, 130, 200))

    game.separator(sx2, sy + 150, 218)
    game.draw_text(sx2, sy + 162, "Spinner: click -/+", g.COLOR_LIGHT_GRAY)
    game.draw_text(sx2, sy + 176, "Knob: drag up/down", g.COLOR_LIGHT_GRAY)

    # Progress Bars
    sx3 = px + 2 * (pw + gap) + 10
    game.draw_text(sx3, sy, "VOLUME:", g.COLOR_WHITE)
    game.progress_bar(sx3, sy + 14, 260, 16, state["volume"], 100, g.COLOR_RGB(52, 150, 92))

    game.draw_text(sx3, sy + 46, "BRIGHTNESS:", g.COLOR_WHITE)
    game.progress_bar(sx3, sy + 60, 260, 16, state["brightness"], 100, g.COLOR_RGB(70, 130, 200))

    game.draw_text(sx3, sy + 92, "SPEED:", g.COLOR_WHITE)
    game.progress_bar(sx3, sy + 106, 260, 16, state["speed"], 100, g.COLOR_RGB(196, 142, 46))

    hp_color = g.COLOR_RGB(52, 180, 92) if state["hp"] > 500 else g.COLOR_RGB(200, 76, 76)
    game.draw_text(sx3, sy + 140, "HP:", g.COLOR_WHITE)
    game.progress_bar(sx3, sy + 154, 260, 16, state["hp"], 999, hp_color)

    game.draw_text(sx3, sy + 186, "KNOB:", g.COLOR_WHITE)
    game.progress_bar(sx3, sy + 200, 260, 16, state["knob_val"], 100, g.COLOR_RGB(70, 130, 200))

    game.separator(sx3, sy + 230, 260)
    game.draw_text(sx3, sy + 242, "Bars driven by", g.COLOR_LIGHT_GRAY)
    game.draw_text(sx3, sy + 256, "slider/knob values.", g.COLOR_LIGHT_GRAY)


def draw_input_tab(game: g.GameLib, cx: int, cy: int, state: dict[str, Any]) -> None:
    pw = 240
    gap = 8
    px = cx + 4

    draw_panel(game, px, cy, pw, 280, "Text Input")
    draw_panel(game, px + pw + gap, cy, pw, 280, "Dropdown")
    draw_panel(game, px + 2 * (pw + gap), cy, pw + 50, 280, "TabBar & Tooltip")

    # Text Input
    tx, ty = px + 10, cy + 30
    game.draw_text(tx, ty, "NAME:", g.COLOR_WHITE)
    _, state["player_name"], state["name_focused"] = game.text_input(
        tx + 50,
        ty - 4,
        160,
        state["player_name"],
        state["name_focused"],
    )
    game.draw_text(tx, ty + 18, f"Hello, {state['player_name']}!", g.COLOR_YELLOW)

    game.draw_text(tx, ty + 50, "SEARCH:", g.COLOR_WHITE)
    _, state["search_text"], state["search_focused"] = game.text_input(
        tx + 56,
        ty + 46,
        154,
        state["search_text"],
        state["search_focused"],
    )
    if state["search_text"]:
        game.draw_text(tx, ty + 68, f"Query: {state['search_text']}", g.COLOR_LIGHT_GRAY)
    else:
        game.draw_text(tx, ty + 68, "Type to search...", g.COLOR_GRAY)

    game.separator(tx, ty + 96, 218)
    game.draw_text(tx, ty + 108, "Click field to focus,", g.COLOR_LIGHT_GRAY)
    game.draw_text(tx, ty + 122, "BACKSPACE to delete.", g.COLOR_LIGHT_GRAY)

    # Dropdown
    dx, dy = px + pw + gap + 10, cy + 30
    game.draw_text(dx, dy, "RESOLUTION:", g.COLOR_WHITE)
    _, state["resolution_idx"], state["resolution_open"] = game.dropdown(
        dx,
        dy + 14,
        218,
        state["resolutions"],
        state["resolution_idx"],
        state["resolution_open"],
    )
    game.draw_text(dx, dy + 54, "QUALITY:", g.COLOR_WHITE)
    _, state["quality_idx"], state["quality_open"] = game.dropdown(
        dx,
        dy + 68,
        218,
        state["qualities"],
        state["quality_idx"],
        state["quality_open"],
    )
    game.separator(dx, dy + 108, 218)
    game.draw_text(dx, dy + 120, f"Res: {state['resolutions'][state['resolution_idx']]}", g.COLOR_LIGHT_GRAY)
    game.draw_text(dx, dy + 136, f"Quality: {state['qualities'][state['quality_idx']]}", g.COLOR_LIGHT_GRAY)

    # TabBar & Tooltip
    tabx, taby = px + 2 * (pw + gap) + 10, cy + 30
    _, state["inner_tab"] = game.tab_bar(tabx, taby, 280, state["tab_names"], state["inner_tab"])
    game.fill_rect(tabx, taby + 26, 280, 60, g.COLOR_RGB(58, 68, 92))
    tab_contents = ["General settings", "Graphics options", "Audio settings", "Key bindings"]
    game.draw_text(tabx + 10, taby + 34, state["tab_names"][state["inner_tab"]], g.COLOR_YELLOW)
    game.draw_text(tabx + 10, taby + 50, tab_contents[state["inner_tab"]], g.COLOR_LIGHT_GRAY)
    game.draw_text(tabx + 10, taby + 66, f"Tab {state['inner_tab'] + 1}/{len(state['tab_names'])}", g.COLOR_WHITE)

    # Tooltip demo
    game.separator(tabx, taby + 106, 280)
    game.draw_text(tabx, taby + 118, "Hover button for tip:", g.COLOR_LIGHT_GRAY)
    if game.button(tabx, taby + 136, 120, 24, "HOVER ME", g.COLOR_RGB(100, 80, 160)):
        state["last_event"] = "HOVER BTN"
    mx, my = game.get_mouse_x(), game.get_mouse_y()
    if g.GameLib.point_in_rect(mx, my, tabx, taby + 136, 120, 24):
        game.tooltip(mx + 12, my + 12, "Click to trigger!")

    if game.button(tabx + 140, taby + 136, 120, 24, "TIP BUTTON", g.COLOR_RGB(80, 120, 160)):
        state["last_event"] = "TIP BTN"
    if g.GameLib.point_in_rect(mx, my, tabx + 140, taby + 136, 120, 24):
        game.tooltip(mx + 12, my + 12, "Another tooltip!")


def draw_advanced_tab(game: g.GameLib, cx: int, cy: int, state: dict[str, Any]) -> None:
    pw = 175
    gap = 8
    px = cx + 4

    draw_panel(game, px, cy, pw, 280, "ListBox")
    draw_panel(game, px + pw + gap, cy, pw, 280, "ColorPicker")
    draw_panel(game, px + 2 * (pw + gap), cy, pw, 280, "Collapsible")
    draw_panel(game, px + 3 * (pw + gap), cy, pw + 30, 280, "ImageButton & Menu")

    # ListBox
    lx, ly = px + 6, cy + 26
    _, state["list_idx"], state["list_scroll"] = game.list_box(
        lx,
        ly,
        pw - 12,
        200,
        state["list_items"],
        state["list_idx"],
        state["list_scroll"],
    )
    game.draw_text(lx, ly + 210, f"Selected: {state['list_items'][state['list_idx']]}", g.COLOR_YELLOW)
    game.draw_text(lx, ly + 228, "Scroll with wheel", g.COLOR_LIGHT_GRAY)

    # ColorPicker
    cpx, cpy = px + pw + gap + 6, cy + 26
    _, state["color_idx"] = game.color_picker(cpx, cpy, state["color_palette"], state["color_idx"])
    sel_color = state["color_palette"][state["color_idx"]]
    game.fill_rect(cpx, cpy + 70, pw - 12, 18, sel_color)
    game.draw_rect(cpx, cpy + 70, pw - 12, 18, g.COLOR_RGB(84, 94, 120))
    r_v = g.COLOR_GET_R(sel_color)
    g_v = g.COLOR_GET_G(sel_color)
    b_v = g.COLOR_GET_B(sel_color)
    game.draw_text(cpx, cpy + 96, f"R:{r_v} G:{g_v} B:{b_v}", g.COLOR_LIGHT_GRAY)
    game.draw_text(cpx, cpy + 112, f"#{sel_color:08X}", g.COLOR_LIGHT_GRAY)

    # Collapsible
    clx, cly = px + 2 * (pw + gap) + 6, cy + 26
    _, state["section_open"] = game.collapsible(clx, cly, pw - 12, "DETAILS", state["section_open"])
    if state["section_open"]:
        game.fill_rect(clx, cly + 22, pw - 12, 50, g.COLOR_RGB(40, 46, 62))
        game.draw_text(clx + 8, cly + 30, "Expanded content", g.COLOR_LIGHT_GRAY)
        game.draw_text(clx + 8, cly + 44, "inside section", g.COLOR_LIGHT_GRAY)
    _, state["section2_open"] = game.collapsible(clx, cly + 80, pw - 12, "EXTRA", state["section2_open"])
    if state["section2_open"]:
        game.fill_rect(clx, cly + 102, pw - 12, 36, g.COLOR_RGB(40, 46, 62))
        game.draw_text(clx + 8, cly + 110, "More content", g.COLOR_LIGHT_GRAY)
    game.separator(clx, cly + 150, pw - 12)
    game.draw_text(clx, cly + 162, "Click header to", g.COLOR_LIGHT_GRAY)
    game.draw_text(clx, cly + 176, "toggle open/close.", g.COLOR_LIGHT_GRAY)

    # ImageButton & Menu
    ibx, iby = px + 3 * (pw + gap) + 6, cy + 26
    if game.image_button(ibx, iby, 50, 50, state["icon_id"], g.COLOR_RGB(60, 70, 100)):
        state["last_event"] = "IMAGE BTN"
    game.draw_text(ibx + 60, iby + 10, "ImageButton", g.COLOR_WHITE)
    game.draw_text(ibx + 60, iby + 26, "with sprite", g.COLOR_LIGHT_GRAY)

    game.separator(ibx, iby + 66, pw + 18)
    if game.button(ibx, iby + 78, 120, 24, "OPEN MENU", g.COLOR_RGB(80, 120, 160)):
        state["menu_open"] = True
    menu_result, state["menu_open"] = game.menu(ibx, iby + 108, state["menu_items"], state["menu_open"])
    if menu_result >= 0:
        state["menu_result"] = menu_result
        state["last_event"] = f"MENU: {state['menu_items'][menu_result]}"
    game.draw_text(ibx, iby + 118, "Last pick:", g.COLOR_WHITE)
    if state["menu_result"] >= 0:
        game.draw_text(ibx, iby + 134, state["menu_items"][state["menu_result"]], g.COLOR_YELLOW)
    game.draw_text(ibx, iby + 164, "Click outside to", g.COLOR_LIGHT_GRAY)
    game.draw_text(ibx, iby + 178, "dismiss menu.", g.COLOR_LIGHT_GRAY)


def draw_status_tab(game: g.GameLib, cx: int, cy: int, state: dict[str, Any]) -> None:
    pw = 240
    gap = 8
    px = cx + 4

    draw_panel(game, px, cy, pw, 280, "Events")
    draw_panel(game, px + pw + gap, cy, pw, 280, "Counts & Flags")
    draw_panel(game, px + 2 * (pw + gap), cy, pw + 50, 280, "All States")

    # Events
    ex, ey = px + 10, cy + 28
    game.label(ex, ey, 218, 20, "LAST EVENT", g.COLOR_RGB(38, 48, 72), g.COLOR_WHITE)
    game.label(ex, ey + 28, 218, 20, state["last_event"], g.COLOR_RGB(52, 60, 82), g.COLOR_YELLOW)
    game.separator(ex, ey + 60, 218)
    game.draw_text(ex, ey + 72, "Interact with any", g.COLOR_LIGHT_GRAY)
    game.draw_text(ex, ey + 86, "control to see its", g.COLOR_LIGHT_GRAY)
    game.draw_text(ex, ey + 100, "event name here.", g.COLOR_LIGHT_GRAY)

    # Counts & Flags
    fx, fy = px + pw + gap + 10, cy + 28
    game.draw_text(fx, fy, "COUNTS", g.COLOR_WHITE)
    game.draw_printf(fx, fy + 16, g.COLOR_LIGHT_GRAY, f"START: {state['start_count']}")
    game.draw_printf(fx, fy + 32, g.COLOR_LIGHT_GRAY, f"RESET: {state['reset_count']}")

    game.separator(fx, fy + 56, 218)
    game.draw_text(fx, fy + 68, "FLAGS", g.COLOR_WHITE)
    game.draw_printf(fx, fy + 84, g.COLOR_LIGHT_GRAY, f"MUSIC: {'ON' if state['music_on'] else 'OFF'}")
    game.draw_printf(fx, fy + 100, g.COLOR_LIGHT_GRAY, f"SFX:   {'ON' if state['sfx_on'] else 'OFF'}")
    game.draw_printf(fx, fy + 116, g.COLOR_LIGHT_GRAY, f"GRID:  {'ON' if state['show_grid'] else 'OFF'}")
    game.draw_printf(fx, fy + 132, g.COLOR_LIGHT_GRAY, f"HARD:  {'ON' if state['hard_mode'] else 'OFF'}")

    # All States
    sx, sy = px + 2 * (pw + gap) + 10, cy + 28
    diff_names = ["EASY", "MEDIUM", "HARD"]
    game.draw_text(sx, sy, "CURRENT VALUES", g.COLOR_WHITE)
    game.draw_printf(sx, sy + 16, g.COLOR_LIGHT_GRAY, f"Volume:     {state['volume']}")
    game.draw_printf(sx, sy + 32, g.COLOR_LIGHT_GRAY, f"Brightness: {state['brightness']}")
    game.draw_printf(sx, sy + 48, g.COLOR_LIGHT_GRAY, f"Speed:      {state['speed']}")
    game.draw_printf(sx, sy + 64, g.COLOR_LIGHT_GRAY, f"HP:         {state['hp']}")
    game.draw_printf(sx, sy + 80, g.COLOR_LIGHT_GRAY, f"Level:      {state['level']}")
    game.draw_printf(sx, sy + 96, g.COLOR_LIGHT_GRAY, f"ScoreMult:  {state['score_mult']}")
    game.draw_printf(sx, sy + 112, g.COLOR_LIGHT_GRAY, f"Knob:       {state['knob_val']}")
    game.separator(sx, sy + 136, 260)
    game.draw_printf(sx, sy + 148, g.COLOR_LIGHT_GRAY, f"Diff:  {diff_names[state['difficulty']]}")
    game.draw_printf(
        sx,
        sy + 164,
        g.COLOR_LIGHT_GRAY,
        f"Pause: {'Y' if state['paused'] else 'N'} Turbo: {'Y' if state['turbo'] else 'N'}",
    )
    game.draw_printf(sx, sy + 180, g.COLOR_LIGHT_GRAY, f"Res:   {state['resolutions'][state['resolution_idx']]}")
    game.draw_printf(sx, sy + 196, g.COLOR_LIGHT_GRAY, f"Name:  {state['player_name']}")


def _reset_all(state: dict[str, Any]) -> None:
    state["music_on"] = True
    state["sfx_on"] = True
    state["show_grid"] = False
    state["hard_mode"] = False
    state["difficulty"] = 0
    state["paused"] = False
    state["turbo"] = False
    state["volume"] = 75
    state["brightness"] = 50
    state["speed"] = 30
    state["hp"] = 100
    state["level"] = 1
    state["score_mult"] = 1
    state["player_name"] = "Player1"
    state["search_text"] = ""
    state["resolution_idx"] = 0
    state["quality_idx"] = 1
    state["inner_tab"] = 0
    state["knob_val"] = 50
    state["color_idx"] = 0
    state["list_idx"] = 0
    state["list_scroll"] = 0
    state["section_open"] = True
    state["section2_open"] = False
    state["menu_result"] = -1
    state["menu_open"] = False
    state["reset_count"] += 1
    state["last_event"] = "RESET"


def main() -> None:
    game = g.GameLib()
    game.open(WIN_W, WIN_H, "15 - Tabbed UI Controls", True)

    # create sprite for image_button demo
    icon_id = game.create_sprite(20, 20)
    for py in range(20):
        for px in range(20):
            c = g.COLOR_RGB(px * 12, py * 12, 200) if (px + py) % 2 == 0 else g.COLOR_RGB(40, 40, 60)
            game.set_sprite_pixel(icon_id, px, py, c)

    state = {
        "music_on": True,
        "sfx_on": True,
        "show_grid": False,
        "hard_mode": False,
        "difficulty": 0,
        "paused": False,
        "turbo": False,
        "start_count": 0,
        "reset_count": 0,
        "last_event": "NONE",
        "quit": False,
        "volume": 75,
        "brightness": 50,
        "speed": 30,
        "hp": 100,
        "level": 1,
        "score_mult": 1,
        "knob_val": 50,
        "player_name": "Player1",
        "name_focused": False,
        "search_text": "",
        "search_focused": False,
        "resolution_idx": 0,
        "resolution_open": False,
        "quality_idx": 1,
        "quality_open": False,
        "inner_tab": 0,
        "resolutions": ["640x480", "800x600", "1024x768", "1280x720", "1920x1080"],
        "qualities": ["LOW", "MEDIUM", "HIGH", "ULTRA"],
        "tab_names": ["GENERAL", "GRAPHICS", "AUDIO", "CONTROLS"],
        "list_items": [
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
        ],
        "list_idx": 0,
        "list_scroll": 0,
        "section_open": True,
        "section2_open": False,
        "color_palette": [
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
        ],
        "color_idx": 0,
        "menu_open": False,
        "menu_result": -1,
        "menu_items": ["NEW GAME", "LOAD GAME", "OPTIONS", "CREDITS", "QUIT"],
        "icon_id": icon_id,
    }

    active_tab = 0
    tab_names = ["BASIC", "VALUES", "INPUT", "ADVANCED", "STATUS"]

    while not game.is_closed():
        if game.is_key_pressed(g.KEY_ESCAPE):
            break
        if state["quit"]:
            break

        draw_backdrop(game)

        # Title bar
        game.fill_rect(0, 0, WIN_W, 44, g.COLOR_RGB(10, 14, 24))
        game.draw_text_scale(16, 10, "UI CONTROLS", g.COLOR_WHITE, 14, 14)
        game.draw_text(16, 30, f"Tab: {tab_names[active_tab]}  |  ESC quits", g.COLOR_LIGHT_GRAY)

        # Main TabPanel
        active_tab, cx, cy, cw, ch = game.tab_panel(20, 52, WIN_W - 40, WIN_H - 62, tab_names, active_tab)

        if active_tab == 0:
            draw_basic_tab(game, cx, cy, state)
        elif active_tab == 1:
            draw_values_tab(game, cx, cy, state)
        elif active_tab == 2:
            draw_input_tab(game, cx, cy, state)
        elif active_tab == 3:
            draw_advanced_tab(game, cx, cy, state)
        elif active_tab == 4:
            draw_status_tab(game, cx, cy, state)

        game.update()
        game.wait_frame(60)


if __name__ == "__main__":
    main()
