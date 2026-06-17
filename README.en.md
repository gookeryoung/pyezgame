# pyezgame

[![PyPI](https://img.shields.io/pypi/v/pyezgame.svg)](https://pypi.org/project/pyezgame/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](pyproject.toml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](clib/LICENSE)

> **Write 2D games in Python — zero configuration, ready to go.**

pyezgame provides Python bindings for [GameLib](https://github.com/skywind3000/GameLib), covering windowing, drawing, sprites, sound, input, tilemaps, scene management, 20+ UI controls, save/load, and more.

```bash
pip install pyezgame
```


## 30-Second Quick Start

```python
import pyezgame as g

game = g.GameLib()
game.open(640, 480, "My Game", True)

x, y = 320, 240

while not game.is_closed():
    if game.is_key_down(g.KEY_LEFT):
        x -= 3
    if game.is_key_down(g.KEY_RIGHT):
        x += 3
    if game.is_key_down(g.KEY_UP):
        y -= 3
    if game.is_key_down(g.KEY_DOWN):
        y += 3

    game.clear(g.COLOR_BLACK)
    game.fill_circle(x, y, 15, g.COLOR_CYAN)
    game.draw_text(10, 10, "Arrow keys to move!", g.COLOR_WHITE)
    game.update()
    game.wait_frame(60)
```


## Features

| | |
|-|-|
| **One-command install** | `pip install pyezgame` — prebuilt wheels for Windows / Linux / macOS |
| **Complete API** | Windowing, drawing, sprites, sound, input, tilemaps, scene management, UI controls, save/load |
| **Pythonic** | C++ `PascalCase` → Python `snake_case`, multi-returns auto-converted to `tuple` |
| **Type hints** | Full `.pyi` type stubs for IDE auto-completion |
| **18 examples** | From Hello World to Magic Tower RPG, progressive and independently runnable |
| **CLI tool** | `ezgame list` / `ezgame run 01` to browse and run examples |

**Platform support:**

| Platform | Backend | Compiler |
|-|-|-|
| Windows | Win32 GDI (no external deps) | MSVC 2015+ / MinGW-w64 |
| Linux | SDL2 | GCC 4.9+ / Clang |
| macOS | SDL2 | Apple Clang |

Prebuilt wheels available for Python 3.9 ~ 3.14 (64-bit).


## Examples

The `examples/` directory contains 18 progressive examples, each independently runnable:

| Example | Description | Key APIs |
|-|-|-|
| `01_hello.py` | Hello World | Game loop, window, text |
| `02_movement.py` | Keyboard movement + bouncing ball | Keyboard input, delta time |
| `03_shapes.py` | All shapes showcase | Lines, rectangles, circles, triangles |
| `04_paint.py` | Simple paint program | Mouse input, scroll wheel |
| `05_sprites.py` | Sprites + frame animation | load_sprite, directional animation |
| `06_sound.py` | Sound playback | play_beep, play_wav, play_music |
| `07_shooting.py` | Simple shooter | Bullet firing, collision |
| `08_breakout.py` | Breakout | Collision detection, multi-object |
| `09_snake.py` | Snake | draw_grid / fill_cell, state machine |
| `10_tilemap.py` | Parallax scrolling | Tilemap, parallax |
| `11_font_text.py` | Scalable fonts | draw_text_font, show_message |
| `12_sprite_transform.py` | Sprite transforms | Scaling / rotation |
| `13_clip_rect.py` | Clip rectangle | set_clip / clear_clip |
| `14_space_shooter.py` | Space Shooter | Comprehensive project |
| `15_ui_controls.py` | UI controls demo | 20+ immediate-mode UI controls |
| `16_conway.py` | Conway's Game of Life | Cellular automata |
| `17_tetris.py` | Tetris | Complete game logic |
| `18_magic_tower.py` | Magic Tower RPG | Tilemap + scene management |

```bash
ezgame list          # List all examples
ezgame run snake     # Run by keyword
python examples/01_hello.py  # Run directly
```


## API Reference

Python bindings follow `snake_case` naming, mapping one-to-one with C++ `PascalCase`.

### Window & Main Loop

| Method | Description |
|-|-|
| `open(w, h, title, center, resizable)` | Create window; `w/h` sets framebuffer logical size |
| `is_closed()` | Whether the window is closed |
| `update()` | Refresh display and process input, call once per frame |
| `wait_frame(fps)` | Frame rate control |
| `get_delta_time()` | Frame interval (seconds) |
| `get_fps()` | Current frame rate |
| `get_time()` | Total elapsed time (seconds) |
| `get_width()` / `get_height()` | Framebuffer logical dimensions |
| `win_resize(w, h)` | Set window client area size |
| `set_maximized(maximized)` | Maximize or restore a resizable window |
| `set_title(title)` | Change window title |
| `show_fps(show)` | Show real-time FPS in title bar |
| `show_mouse(show)` | Show or hide mouse cursor |
| `aspect_lock(lock, color)` | Lock aspect ratio, fill letterbox with color |
| `show_message(text, title, buttons)` | Show message box |

### Drawing

| Method | Description |
|-|-|
| `clear(color)` | Clear screen |
| `set_pixel(x, y, color)` | Draw pixel (Alpha blending supported) |
| `get_pixel(x, y)` | Read pixel |
| `set_clip(x, y, w, h)` | Set clip rectangle |
| `clear_clip()` | Clear clip, restore full screen |
| `get_clip()` | Get current clip rectangle `(x, y, w, h)` |
| `get_clip_x()` / `get_clip_y()` / `get_clip_w()` / `get_clip_h()` | Get clip rectangle components |
| `screenshot(filename)` | Save current frame as BMP |
| `draw_line(x1, y1, x2, y2, color)` | Draw line |
| `draw_rect(x, y, w, h, color)` | Rectangle outline |
| `fill_rect(x, y, w, h, color)` | Filled rectangle |
| `draw_circle(cx, cy, r, color)` | Circle outline |
| `fill_circle(cx, cy, r, color)` | Filled circle |
| `draw_ellipse(cx, cy, rx, ry, color)` | Ellipse outline |
| `fill_ellipse(cx, cy, rx, ry, color)` | Filled ellipse |
| `draw_triangle(x1, y1, x2, y2, x3, y3, color)` | Triangle outline |
| `fill_triangle(x1, y1, x2, y2, x3, y3, color)` | Filled triangle |

### Text

| Method | Description |
|-|-|
| `draw_text(x, y, text, color)` | Built-in 8x8 font |
| `draw_number(x, y, number, color)` | Draw integer |
| `draw_text_scale(x, y, text, color, w, h)` | Scaled text (each char w×h px) |
| `draw_printf(x, y, color, text)` | Formatted output (use f-strings) |
| `draw_printf_scale(x, y, color, w, h, text)` | Scaled formatted output |
| `draw_text_font(x, y, text, color, size)` | Scalable font (UTF-8) |
| `draw_text_font(x, y, text, color, font, size)` | Named font |
| `get_text_width_font(...)` / `get_text_height_font(...)` | Measure text dimensions |

### Sprite System

| Method | Description |
|-|-|
| `create_sprite(w, h)` | Create blank sprite, returns ID |
| `load_sprite(filename)` | Load image (PNG/JPG/BMP/GIF/TIFF) |
| `load_sprite_bmp(filename)` | Load from BMP |
| `free_sprite(id)` | Free sprite |
| `draw_sprite(id, x, y)` | Draw sprite (opaque fast path) |
| `draw_sprite_ex(id, x, y, flags)` | Draw with flip/transparency/alpha |
| `draw_sprite_region(id, x, y, sx, sy, sw, sh)` | Draw sprite sub-region |
| `draw_sprite_region_ex(id, x, y, sx, sy, sw, sh, flags)` | Sub-region with flags |
| `draw_sprite_scaled(id, x, y, w, h, flags)` | Scaled draw |
| `draw_sprite_rotated(id, cx, cy, angle, flags)` | Rotated draw |
| `draw_sprite_frame(id, x, y, fw, fh, index, flags)` | Sprite sheet frame |
| `draw_sprite_frame_scaled(...)` | Scaled frame |
| `draw_sprite_frame_rotated(...)` | Rotated frame |
| `set_sprite_pixel(id, x, y, color)` | Modify sprite pixel |
| `get_sprite_pixel(id, x, y)` | Read sprite pixel |
| `get_sprite_width(id)` / `get_sprite_height(id)` | Read sprite dimensions |
| `set_sprite_color_key(id, color)` | Set Color Key |
| `get_sprite_color_key(id)` | Get Color Key |

Sprite flags: `SPRITE_FLIP_H`, `SPRITE_FLIP_V`, `SPRITE_COLORKEY`, `SPRITE_ALPHA`

> **Note**: `draw_sprite(id, x, y)` uses the opaque fast path. For transparency, explicitly pass `SPRITE_COLORKEY` or `SPRITE_ALPHA`.

### Input

| Method | Description |
|-|-|
| `is_key_down(key)` | Key held down |
| `is_key_pressed(key)` | Key just pressed (edge trigger) |
| `is_key_released(key)` | Key just released (edge trigger) |
| `get_mouse_x()` / `get_mouse_y()` | Mouse position (auto-mapped to framebuffer) |
| `is_mouse_down(button)` | Mouse button held |
| `is_mouse_pressed(button)` | Mouse button just pressed |
| `is_mouse_released(button)` | Mouse button just released |
| `get_mouse_wheel_delta()` | Scroll wheel delta |
| `is_active()` | Window has focus |

### Sound

| Method | Description |
|-|-|
| `play_wav(filename, repeat, volume)` | Play WAV, returns channel ID |
| `play_beep(freq, duration, repeat, volume)` | Beep tone, returns channel ID |
| `stop_wav(channel)` | Stop channel |
| `is_playing(channel)` | Query channel status |
| `set_volume(channel, volume)` | Set channel volume (0-1000) |
| `stop_all()` | Stop all sounds |
| `set_master_volume(volume)` | Set master volume (0-1000) |
| `get_master_volume()` | Get master volume |
| `play_music(filename, loop)` | Background music (MP3/MIDI/WAV) |
| `stop_music()` | Stop music |
| `is_music_playing()` | Music playing? |

### Tilemap

| Method | Description |
|-|-|
| `create_tilemap(cols, rows, tile_size, tileset_id)` | Create tilemap |
| `save_tilemap(filename, map_id)` | Save to `.glm` |
| `load_tilemap(filename, tileset_id)` | Load from `.glm` |
| `free_tilemap(map_id)` | Free map |
| `set_tile(map_id, col, row, tile_id)` | Set tile (-1=empty) |
| `get_tile(map_id, col, row)` | Read tile |
| `get_tilemap_cols(map_id)` / `get_tilemap_rows(map_id)` | Map dimensions |
| `get_tile_size(map_id)` | Tile size |
| `world_to_tile_col(map_id, x)` / `world_to_tile_row(map_id, y)` | Pixel to tile coords |
| `get_tile_at_pixel(map_id, x, y)` | Read tile at pixel |
| `fill_tile_rect(map_id, col, row, cols, rows, tile_id)` | Batch fill |
| `clear_tilemap(map_id, tile_id)` | Clear map |
| `draw_tilemap(map_id, x, y, flags)` | Draw map (pass `-camX, -camY` for scrolling) |

### Scene Management

| Method | Description |
|-|-|
| `set_scene(scene)` | Switch scene (next frame) |
| `get_scene()` | Current scene |
| `is_scene_changed()` | Just entered new scene |
| `get_previous_scene()` | Previous scene |

### UI Controls

All UI controls are immediate-mode: call once per frame to draw and handle interaction.

**Basic:**

| Method | Description |
|-|-|
| `button(x, y, w, h, text, color)` | Button, returns `True` on click |
| `checkbox(x, y, text, checked)` | Checkbox → `(triggered, checked)` |
| `radio_box(x, y, text, value, index)` | Radio → `(triggered, value)` |
| `toggle_button(x, y, w, h, text, toggled, color)` | Toggle → `(triggered, toggled)` |
| `slider(x, y, w, value, min_val, max_val)` | Slider → `(changed, value)` |
| `progress_bar(x, y, w, h, value, max_val, color)` | Progress bar |
| `spinner(x, y, w, value, min_val, max_val, step)` | Spinner → `(changed, value)` |
| `knob(x, y, size, value, min_val, max_val)` | Knob → `(changed, value)` |
| `separator(x, y, w)` | Horizontal separator |
| `v_separator(x, y, h)` | Vertical separator |
| `label(x, y, w, h, text, bg_color, text_color)` | Text label |

**Input & Selection:**

| Method | Description |
|-|-|
| `text_input(x, y, w, buffer, focused)` | Text input → `(changed, text, focused)` |
| `dropdown(x, y, w, items, selected_index, open)` | Dropdown → `(changed, selected_index, open)` |
| `list_box(x, y, w, h, items, selected_index, scroll_offset)` | List box → `(changed, selected_index, scroll_offset)` |
| `color_picker(x, y, colors, selected_index)` | Color picker → `(changed, selected_index)` |

**Navigation & Layout:**

| Method | Description |
|-|-|
| `tab_bar(x, y, w, tabs, selected_tab)` | Tab bar → `(changed, selected_tab)` |
| `tab_panel(x, y, w, h, tabs, selected_tab)` | Tab panel → `(active_tab, cx, cy, cw, ch)` |
| `collapsible(x, y, w, title, open)` | Collapsible → `(triggered, open)` |
| `menu(x, y, items, open)` | Popup menu → `(selected_index, open)` |

**Other:** `tooltip(x, y, text)` tooltip overlay · `image_button(x, y, w, h, sprite_id, color)` sprite button

> **Tip**: `tab_panel` returns `(cx, cy, cw, ch)` — the content area rectangle for placing child controls.

### Grid Helpers

| Method | Description |
|-|-|
| `draw_grid(x, y, rows, cols, cell_size, color)` | Draw grid |
| `fill_cell(grid_x, grid_y, row, col, cell_size, color)` | Fill grid cell |

### Save / Load (Static)

| Method | Description |
|-|-|
| `GameLib.save_int(filename, key, value)` | Save integer |
| `GameLib.save_float(filename, key, value)` | Save float |
| `GameLib.save_string(filename, key, value)` | Save string |
| `GameLib.load_int(filename, key, default)` | Load integer |
| `GameLib.load_float(filename, key, default)` | Load float |
| `GameLib.load_string(filename, key, default)` | Load string |
| `GameLib.has_save_key(filename, key)` | Key exists? |
| `GameLib.delete_save_key(filename, key)` | Delete key |
| `GameLib.delete_save(filename)` | Delete save file |

### Utility Methods (Static)

| Method | Description |
|-|-|
| `GameLib.random(min, max)` | Random int `[min, max]` |
| `GameLib.rect_overlap(x1, y1, w1, h1, x2, y2, w2, h2)` | AABB collision |
| `GameLib.circle_overlap(cx1, cy1, r1, cx2, cy2, r2)` | Circle collision |
| `GameLib.point_in_rect(px, py, x, y, w, h)` | Point in rect |
| `GameLib.distance(x1, y1, x2, y2)` | Distance between points |

### Color Constants

```
COLOR_BLACK    COLOR_WHITE     COLOR_RED       COLOR_GREEN     COLOR_BLUE
COLOR_YELLOW   COLOR_CYAN      COLOR_MAGENTA   COLOR_ORANGE    COLOR_PINK
COLOR_PURPLE   COLOR_GRAY      COLOR_DARK_GRAY COLOR_LIGHT_GRAY
COLOR_DARK_RED COLOR_DARK_GREEN COLOR_DARK_BLUE COLOR_SKY_BLUE
COLOR_BROWN    COLOR_GOLD      COLOR_TRANSPARENT
```

Custom: `COLOR_RGB(r, g, b)` / `COLOR_ARGB(a, r, g, b)`

Extract: `COLOR_GET_A(c)` / `COLOR_GET_R(c)` / `COLOR_GET_G(c)` / `COLOR_GET_B(c)`

### Utility Functions

| Function | Description |
|-|-|
| `get_respath(*parts)` | Absolute path to package resource (POSIX) |
| `get_asset_path(filename)` | Absolute path to `clib/assets/` file (POSIX) |
| `clamp(value, lo, hi)` | Clamp into `[lo, hi]` |
| `safe_dt(game, max_dt)` | Capped delta time (default cap: 0.05s) |
| `draw_checkerboard(game, x, y, w, h, cell)` | Checkerboard pattern |
| `draw_panel(game, x, y, w, h, title)` | Panel with title bar |


## Building from Source

**Requirements:** Python 3.9+, C++14 compiler (MSVC 2015+ / GCC 4.9+ / Clang), CMake 3.15+

```bash
git clone --recursive <repo-url> && cd pyezgame
pip install .

# Or development mode
pip install -e . --no-build-isolation
```

Linux / macOS require SDL2 dev packages:

```bash
# Ubuntu / Debian
sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-ttf-dev libsdl2-mixer-dev

# macOS
brew install sdl2 sdl2_image sdl2_ttf sdl2_mixer
```


## C++ vs Python Comparison

| C++ (GameLib) | Python (pyezgame) |
|-|-|
| `game.Open(640, 480, "Title", true)` | `game.open(640, 480, "Title", True)` |
| `game.Clear(COLOR_BLACK)` | `game.clear(COLOR_BLACK)` |
| `game.FillCircle(x, y, r, color)` | `game.fill_circle(x, y, r, color)` |
| `game.DrawText(x, y, "hi", color)` | `game.draw_text(x, y, "hi", color)` |
| `game.IsKeyDown(KEY_LEFT)` | `game.is_key_down(KEY_LEFT)` |
| `game.DrawPrintf(x, y, c, "Score: %d", s)` | `game.draw_printf(x, y, c, f"Score: {s}")` |
| `GameLib::Random(0, 100)` | `GameLib.random(0, 100)` |

> C++ `Checkbox(x, y, text, &checked)` modifies via pointer; Python returns `(triggered, checked)` tuple — update the state variable manually.


## Acknowledgments

- [GameLib](https://github.com/skywind3000/GameLib) — C++ game library, single header, zero dependencies
- [pybind11](https://github.com/pybind/pybind11) — C++ / Python interoperability
- [scikit-build-core](https://github.com/scikit-build/scikit-build-core) — Python C extension build system


## License

MIT License
