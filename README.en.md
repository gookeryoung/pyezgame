# pyezgame

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](clib/LICENSE) [![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](pyproject.toml) [![GameLib](https://img.shields.io/badge/GameLib-header--only-green.svg)](clib/GameLib.h)

Python bindings for [GameLib](https://github.com/skywind3000/GameLib) — write 2D games in Python, zero configuration, ready to go out of the box.

pyezgame brings the beginner-friendly C++ game development library [GameLib](https://github.com/skywind3000/GameLib) to Python. Through pybind11 bindings, Python developers can use concise Python syntax to create windows, draw graphics, animate sprites, play sounds, handle keyboard/mouse input, and more — no C++ knowledge required.


## Highlights

- **One-command install** — `pip install .` compiles and installs, handling all C++ build steps automatically
- **Complete API** — covers all GameLib features: windowing, drawing, sprites, sound, input, tilemaps, scene management, UI controls, save/load
- **Pythonic interface** — C++ `PascalCase` methods are converted to Python `snake_case`, with return values adapted to Python conventions (e.g., `tuple` for multiple returns)
- **Type hints** — full `.pyi` type stubs provided, IDE auto-completion friendly
- **18 examples** — from Hello World to Magic Tower RPG, progressive and independently runnable
- **CLI tool** — built-in `ezgame` command line to quickly browse and run examples


## Quick Start

### Installation

Requires Python 3.9+ and a C++14-capable compiler (MSVC or MinGW-w64 recommended on Windows).

```bash
# Clone the repository (with GameLib subdirectory)
git clone --recursive <repo-url>
cd pyezgame

# Install (automatically compiles C++ extension)
pip install .
```

Or using [uv](https://docs.astral.sh/uv/):

```bash
uv sync
uv pip install .
```

### Your First Program

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
    game.draw_text(10, 10, "Up/Down/Left/Right to move!", g.COLOR_WHITE)
    game.update()
    game.wait_frame(60)
```

Run it:

```bash
python my_game.py
```

### Running Built-in Examples

```bash
# List all examples
ezgame list

# Run by number
ezgame run 01

# Run by keyword
ezgame run snake
```

Or run the Python files directly:

```bash
python examples/01_hello.py
python examples/09_snake.py
```


## Examples

The `examples/` directory contains 18 progressive Python examples:

### Getting Started

| Example | Description | What You'll Learn |
|-|-|-|
| `01_hello.py` | Hello World | Game loop, window creation, text drawing |
| `02_movement.py` | Keyboard movement + bouncing ball | Keyboard input, get_delta_time, wall bounce |
| `03_shapes.py` | All shapes showcase | Lines, rectangles, circles, ellipses, triangles (stroke & fill) |
| `04_paint.py` | Simple paint program | Mouse input, scroll wheel brush size, focus-loss pause |

### Sprites and Sound

| Example | Description | What You'll Learn |
|-|-|-|
| `05_sprites.py` | Sprite basics + frame animation | load_sprite, directional animation |
| `06_sound.py` | Sound playback demo | play_beep, play_wav, play_music |
| `07_shooting.py` | Simple shooter | Bullet firing, collision destruction |

### Complete Mini-Games

| Example | Description | What You'll Learn |
|-|-|-|
| `08_breakout.py` | Breakout | Collision detection, multi-object management |
| `09_snake.py` | Snake | draw_grid / fill_cell, state machine |

### Tilemap and Text

| Example | Description | What You'll Learn |
|-|-|-|
| `10_tilemap.py` | Dual-layer parallax scrolling | Tilemap, parallax scrolling |
| `11_font_text.py` | Scalable fonts and UI | draw_text_font, show_message |

### Advanced Features

| Example | Description | What You'll Learn |
|-|-|-|
| `12_sprite_transform.py` | Sprite scaling + rotation | draw_sprite_scaled / draw_sprite_rotated |
| `13_clip_rect.py` | Clip rectangle | set_clip / clear_clip |
| `14_space_shooter.py` | Space Shooter | Comprehensive project |
| `15_ui_controls.py` | UI controls demo | button, checkbox, radio_box, slider, spinner, tab_panel, dropdown, knob, etc. |

### Bonus Examples

| Example | Description | What You'll Learn |
|-|-|-|
| `16_conway.py` | Conway's Game of Life | Cellular automata, grid-based simulation |
| `17_tetris.py` | Tetris | Complete game logic, piece rotation |
| `18_magic_tower.py` | Magic Tower | Tilemap-based RPG, scene management |


## API Reference

Python bindings follow `snake_case` naming, mapping one-to-one with the C++ `PascalCase` API.

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
| `aspect_lock(lock, color)` | Lock aspect ratio, fill letterbox with specified color |
| `show_message(text, title, buttons)` | Show message box |

### Drawing

| Method | Description |
|-|-|
| `clear(color)` | Clear screen |
| `set_pixel(x, y, color)` | Draw pixel (supports Alpha blending) |
| `get_pixel(x, y)` | Read pixel |
| `set_clip(x, y, w, h)` | Set clip rectangle |
| `clear_clip()` | Clear clip, restore full screen |
| `get_clip()` | Get current clip rectangle `(x, y, w, h)` |
| `get_clip_x()` / `get_clip_y()` / `get_clip_w()` / `get_clip_h()` | Get individual clip rectangle components |
| `screenshot(filename)` | Save current frame as BMP file |
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
| `draw_text(x, y, text, color)` | Draw text with built-in 8x8 font |
| `draw_number(x, y, number, color)` | Draw integer |
| `draw_text_scale(x, y, text, color, w, h)` | Draw scaled text (each char w×h pixels) |
| `draw_printf(x, y, color, text)` | Formatted output (use f-strings in Python) |
| `draw_printf_scale(x, y, color, w, h, text)` | Scaled formatted output |
| `draw_text_font(x, y, text, color, size)` | Draw text with scalable font (UTF-8 support) |
| `draw_text_font(x, y, text, color, font, size)` | Draw text with specified font |
| `get_text_width_font(...)` / `get_text_height_font(...)` | Measure text dimensions |

### Sprite System

| Method | Description |
|-|-|
| `create_sprite(w, h)` | Create blank sprite, returns ID |
| `load_sprite(filename)` | Load image sprite (PNG/JPG/BMP/GIF/TIFF) |
| `load_sprite_bmp(filename)` | Load sprite from BMP |
| `free_sprite(id)` | Free sprite |
| `draw_sprite(id, x, y)` | Draw sprite (opaque fast path) |
| `draw_sprite_ex(id, x, y, flags)` | Draw with flip/transparency/alpha blending |
| `draw_sprite_region(id, x, y, sx, sy, sw, sh)` | Draw sprite sub-region |
| `draw_sprite_region_ex(id, x, y, sx, sy, sw, sh, flags)` | Draw sprite sub-region with flags |
| `draw_sprite_scaled(id, x, y, w, h, flags)` | Draw sprite scaled |
| `draw_sprite_rotated(id, cx, cy, angle, flags)` | Draw sprite rotated |
| `draw_sprite_frame(id, x, y, fw, fh, index, flags)` | Draw sprite sheet frame |
| `draw_sprite_frame_scaled(...)` | Draw scaled frame |
| `draw_sprite_frame_rotated(...)` | Draw rotated frame |
| `set_sprite_pixel(id, x, y, color)` | Modify sprite pixel |
| `get_sprite_pixel(id, x, y)` | Read sprite pixel |
| `get_sprite_width(id)` / `get_sprite_height(id)` | Read sprite dimensions |
| `set_sprite_color_key(id, color)` | Set Color Key |
| `get_sprite_color_key(id)` | Get Color Key |

Sprite flags: `SPRITE_FLIP_H` (horizontal flip), `SPRITE_FLIP_V` (vertical flip), `SPRITE_COLORKEY` (Color Key transparency), `SPRITE_ALPHA` (Alpha blending)

> **Note**: `draw_sprite(id, x, y)` uses the opaque fast path by default. If your assets need transparency, explicitly pass `SPRITE_COLORKEY` or `SPRITE_ALPHA`.

### Input

| Method | Description |
|-|-|
| `is_key_down(key)` | Whether key is held down |
| `is_key_pressed(key)` | Whether key was just pressed (single trigger) |
| `is_key_released(key)` | Whether key was just released (single trigger) |
| `get_mouse_x()` / `get_mouse_y()` | Mouse position (auto-mapped to framebuffer coordinates) |
| `is_mouse_down(button)` | Whether mouse button is pressed |
| `is_mouse_pressed(button)` | Whether mouse button was just pressed (single trigger) |
| `is_mouse_released(button)` | Whether mouse button was just released (single trigger) |
| `get_mouse_wheel_delta()` | Scroll wheel delta |
| `is_active()` | Whether the window is currently active |

### Sound

| Method | Description |
|-|-|
| `play_wav(filename, repeat, volume)` | Play WAV sound effect, returns channel ID |
| `play_beep(freq, duration, repeat, volume)` | Beep, returns channel ID |
| `stop_wav(channel)` | Stop specified channel |
| `is_playing(channel)` | Query whether channel is playing |
| `set_volume(channel, volume)` | Set channel volume (0-1000) |
| `stop_all()` | Stop all sound effects |
| `set_master_volume(volume)` | Set master volume (0-1000) |
| `get_master_volume()` | Get master volume |
| `play_music(filename, loop)` | Play background music (MP3/MIDI/WAV) |
| `stop_music()` | Stop background music |
| `is_music_playing()` | Whether music is currently playing |

### Tilemap

| Method | Description |
|-|-|
| `create_tilemap(cols, rows, tile_size, tileset_id)` | Create tile map |
| `save_tilemap(filename, map_id)` | Save to `.glm` file |
| `load_tilemap(filename, tileset_id)` | Load from `.glm` file |
| `free_tilemap(map_id)` | Free map |
| `set_tile(map_id, col, row, tile_id)` | Set tile (-1=empty) |
| `get_tile(map_id, col, row)` | Read tile |
| `get_tilemap_cols(map_id)` / `get_tilemap_rows(map_id)` | Read map dimensions |
| `get_tile_size(map_id)` | Read tile size |
| `world_to_tile_col(map_id, x)` / `world_to_tile_row(map_id, y)` | Convert pixel to tile coordinates |
| `get_tile_at_pixel(map_id, x, y)` | Read tile at pixel position |
| `fill_tile_rect(map_id, col, row, cols, rows, tile_id)` | Batch fill rectangular area |
| `clear_tilemap(map_id, tile_id)` | Clear map |
| `draw_tilemap(map_id, x, y, flags)` | Draw map (pass `-cameraX, -cameraY` for scrolling) |

### Scene Management

| Method | Description |
|-|-|
| `set_scene(scene)` | Switch scene (takes effect next frame) |
| `get_scene()` | Get current scene |
| `is_scene_changed()` | Whether this frame just entered a new scene |
| `get_previous_scene()` | Get previous scene before the switch |

### UI Controls

All UI controls are immediate-mode: call once per frame to draw and handle interaction automatically.

#### Basic Controls

| Method | Description |
|-|-|
| `button(x, y, w, h, text, color)` | Button, returns `True` on click |
| `checkbox(x, y, text, checked)` | Checkbox, returns `(triggered, checked)` |
| `radio_box(x, y, text, value, index)` | Radio button, returns `(triggered, value)` |
| `toggle_button(x, y, w, h, text, toggled, color)` | Toggle button, returns `(triggered, toggled)` |
| `slider(x, y, w, value, min_val, max_val)` | Horizontal slider, returns `(changed, value)` |
| `progress_bar(x, y, w, h, value, max_val, color)` | Progress bar |
| `spinner(x, y, w, value, min_val, max_val, step)` | Numeric spinner, returns `(changed, value)` |
| `knob(x, y, size, value, min_val, max_val)` | Rotary knob, vertical drag to adjust, returns `(changed, value)` |
| `separator(x, y, w)` | Horizontal separator line |
| `v_separator(x, y, h)` | Vertical separator line |
| `label(x, y, w, h, text, bg_color, text_color)` | Centered text label |

#### Input and Selection

| Method | Description |
|-|-|
| `text_input(x, y, w, buffer, focused)` | Text input field, returns `(changed, text, focused)` |
| `dropdown(x, y, w, items, selected_index, open)` | Dropdown combo box, returns `(changed, selected_index, open)` |
| `list_box(x, y, w, h, items, selected_index, scroll_offset)` | Scrollable list box, returns `(changed, selected_index, scroll_offset)` |
| `color_picker(x, y, colors, selected_index)` | Color swatch picker, returns `(changed, selected_index)` |

#### Navigation and Layout

| Method | Description |
|-|-|
| `tab_bar(x, y, w, tabs, selected_tab)` | Tab bar, returns `(changed, selected_tab)` |
| `tab_panel(x, y, w, h, tabs, selected_tab)` | Tabbed panel, returns `(active_tab, cx, cy, cw, ch)` with content area rect |
| `collapsible(x, y, w, title, open)` | Collapsible section header, returns `(triggered, open)` |
| `menu(x, y, items, open)` | Popup menu, returns `(selected_index, open)`, auto-closes on selection or outside click |

#### Other

| Method | Description |
|-|-|
| `tooltip(x, y, text)` | Tooltip overlay |
| `image_button(x, y, w, h, sprite_id, color)` | Image button (sprite instead of text), returns `True` on click |

> **Tip**: `tab_panel` returns `(cx, cy, cw, ch)` which describes the content area rectangle inside the panel — use these coordinates directly to place child controls.

### Grid Helpers

| Method | Description |
|-|-|
| `draw_grid(x, y, rows, cols, cell_size, color)` | Draw a grid of cells |
| `fill_cell(grid_x, grid_y, row, col, cell_size, color)` | Fill a single grid cell |

### Save / Load (Static Methods)

| Method | Description |
|-|-|
| `GameLib.save_int(filename, key, value)` | Save integer |
| `GameLib.save_float(filename, key, value)` | Save float |
| `GameLib.save_string(filename, key, value)` | Save string |
| `GameLib.load_int(filename, key, default)` | Load integer |
| `GameLib.load_float(filename, key, default)` | Load float |
| `GameLib.load_string(filename, key, default)` | Load string |
| `GameLib.has_save_key(filename, key)` | Check if key exists |
| `GameLib.delete_save_key(filename, key)` | Delete a specific key |
| `GameLib.delete_save(filename)` | Delete entire save file |

### Utility Methods (Static)

| Method | Description |
|-|-|
| `GameLib.random(min, max)` | Random number `[min, max]` |
| `GameLib.rect_overlap(x1, y1, w1, h1, x2, y2, w2, h2)` | Rectangle collision detection |
| `GameLib.circle_overlap(cx1, cy1, r1, cx2, cy2, r2)` | Circle collision detection |
| `GameLib.point_in_rect(px, py, x, y, w, h)` | Point inside rectangle |
| `GameLib.distance(x1, y1, x2, y2)` | Distance between two points |

### Color Constants

```
COLOR_BLACK    COLOR_WHITE     COLOR_RED       COLOR_GREEN     COLOR_BLUE
COLOR_YELLOW   COLOR_CYAN      COLOR_MAGENTA   COLOR_ORANGE    COLOR_PINK
COLOR_PURPLE   COLOR_GRAY      COLOR_DARK_GRAY COLOR_LIGHT_GRAY
COLOR_DARK_RED COLOR_DARK_GREEN COLOR_DARK_BLUE COLOR_SKY_BLUE
COLOR_BROWN    COLOR_GOLD      COLOR_TRANSPARENT
```

Custom colors: `COLOR_RGB(r, g, b)` or `COLOR_ARGB(a, r, g, b)`

Color component extraction: `COLOR_GET_A(c)` / `COLOR_GET_R(c)` / `COLOR_GET_G(c)` / `COLOR_GET_B(c)`

### Utility Functions

| Function | Description |
|-|-|
| `get_respath(*parts)` | Get absolute path to a package resource (POSIX format) |
| `get_asset_path(filename)` | Get absolute path to a file in `clib/assets/` (POSIX format) |
| `clamp(value, lo, hi)` | Clamp value into `[lo, hi]` |
| `safe_dt(game, max_dt)` | Get delta time capped at max_dt to prevent frame spikes (default cap: 0.05s) |
| `draw_checkerboard(game, x, y, w, h, cell)` | Draw a checkerboard pattern |
| `draw_panel(game, x, y, w, h, title)` | Draw a panel with a title bar |


## Building from Source

### Prerequisites

- Python 3.8+
- C++11 compiler (MSVC 2015+ / GCC 4.9+ / Clang)
- CMake 3.15+

### Build Steps

```bash
# Install build dependencies
pip install scikit-build-core pybind11

# Build and install
pip install .

# Or development mode
pip install -e . --no-build-isolation
```

Using uv:

```bash
uv sync
uv pip install -e . --no-build-isolation
```


## C++ vs Python API Comparison

| C++ (GameLib) | Python (pyezgame) | Notes |
|-|-|-|
| `game.Open(640, 480, "Title", true)` | `game.open(640, 480, "Title", True)` | Create window |
| `game.IsClosed()` | `game.is_closed()` | Window closed? |
| `game.Clear(COLOR_BLACK)` | `game.clear(COLOR_BLACK)` | Clear screen |
| `game.FillCircle(x, y, r, color)` | `game.fill_circle(x, y, r, color)` | Filled circle |
| `game.DrawText(x, y, "hi", color)` | `game.draw_text(x, y, "hi", color)` | Draw text |
| `game.IsKeyDown(KEY_LEFT)` | `game.is_key_down(KEY_LEFT)` | Key detection |
| `game.Update()` | `game.update()` | Refresh display |
| `game.WaitFrame(60)` | `game.wait_frame(60)` | Frame rate control |
| `game.DrawPrintf(x, y, c, "Score: %d", s)` | `game.draw_printf(x, y, c, f"Score: {s}")` | Use f-strings |
| `GameLib::Random(0, 100)` | `GameLib.random(0, 100)` | Static method |

> The C++ `Checkbox(x, y, text, &checked)` modifies `checked` via pointer; the Python version returns a `(triggered, checked)` tuple — you need to update the state variable manually.


## Project Structure

```
pyezgame/
├── clib/              # GameLib C++ headers (for compilation)
│   ├── GameLib.h      # Win32 version
│   └── GameLib.SDL.h  # SDL2 version
├── pyezgame/          # Python package
│   ├── __init__.py    # Package entry point
│   ├── __init__.pyi   # Type stubs
│   ├── cli.py         # CLI tool
│   └── utils.py       # Utility functions (clamp, safe_dt, etc.)
├── src/
│   └── bindings.cpp   # pybind11 C++ binding code
├── examples/          # Python examples (18)
│   ├── 01_hello.py
│   ├── ...
│   └── 18_magic_tower.py
├── tests/             # Unit tests
├── CMakeLists.txt     # CMake build configuration
└── pyproject.toml     # Python project configuration
```


## What Can You Build?

- Space shooters / side-scrollers / Tetris / Snake / Breakout
- Maze games / fruit catchers / bullet hell
- Turn-based RPGs / visual novels / map editors / paint programs
- Course project demos (zero-config delivery)
- Any 2D game or interactive program you can imagine


## Acknowledgments

- [GameLib](https://github.com/skywind3000/GameLib) — underlying C++ game library, single header, zero dependencies
- [pybind11](https://github.com/pybind/pybind11) — C++ / Python interoperability binding library
- [scikit-build-core](https://github.com/scikit-build/scikit-build-core) — Python C extension build system


## License

MIT License. Use it however you want.
