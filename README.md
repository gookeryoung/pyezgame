# pyezgame

[![PyPI](https://img.shields.io/pypi/v/pyezgame.svg)](https://pypi.org/project/pyezgame/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](pyproject.toml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](clib/LICENSE)

> **用 Python 写 2D 游戏，零配置，即装即用。**

pyezgame 是 [GameLib](https://github.com/skywind3000/GameLib) 的 Python 绑定，覆盖窗口、绘图、精灵、声音、输入、Tilemap、场景管理、20+ UI 控件、存档读写等全部功能。

```bash
pip install pyezgame
```

## 30 秒上手

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


## 特性

| | |
|-|-|
| **一键安装** | `pip install pyezgame`，预编译 wheel 支持 Windows / Linux / macOS |
| **完整 API** | 窗口、绘图、精灵、声音、输入、Tilemap、场景管理、UI 控件、存档读写 |
| **Pythonic** | C++ `PascalCase` → Python `snake_case`，多返回值自动转为 `tuple` |
| **类型提示** | 完整 `.pyi` 类型存根，IDE 自动补全 |
| **18 个示例** | 从 Hello World 到魔塔 RPG，由浅入深 |
| **CLI 工具** | `ezgame list` / `ezgame run 01` 快速浏览和运行示例 |

**平台支持：**

| 平台 | 后端 | 编译器 |
|-|-|-|
| Windows | Win32 GDI（零外部依赖） | MSVC 2015+ / MinGW-w64 |
| Linux | SDL2 | GCC 4.9+ / Clang |
| macOS | SDL2 | Apple Clang |

预编译 wheel 支持 Python 3.9 ~ 3.14（64 位）。


## 示例程序

`examples/` 目录包含 18 个由浅入深的示例，每个可独立运行：

| 示例 | 说明 | 关键 API |
|-|-|-|
| `01_hello.py` | Hello World | 游戏循环、窗口创建、文字绘制 |
| `02_movement.py` | 键盘移动 + 弹跳小球 | 键盘输入、delta time、碰壁反弹 |
| `03_shapes.py` | 图形绘制展示 | 线、矩形、圆、椭圆、三角 |
| `04_paint.py` | 简易画板 | 鼠标输入、滚轮调笔刷 |
| `05_sprites.py` | 精灵 + 帧动画 | load_sprite、方向动画 |
| `06_sound.py` | 声音播放 | play_beep、play_wav、play_music |
| `07_shooting.py` | 简易射击 | 子弹发射、碰撞销毁 |
| `08_breakout.py` | 打砖块 | 碰撞检测、多对象管理 |
| `09_snake.py` | 贪吃蛇 | draw_grid / fill_cell、状态机 |
| `10_tilemap.py` | 视差卷轴 | Tilemap、视差滚动 |
| `11_font_text.py` | 可缩放字体 | draw_text_font、show_message |
| `12_sprite_transform.py` | 精灵变换 | 缩放 / 旋转 |
| `13_clip_rect.py` | 裁剪矩形 | set_clip / clear_clip |
| `14_space_shooter.py` | 太空射击 | 综合实战 |
| `15_ui_controls.py` | UI 控件演示 | 20+ 种立即模式 UI 控件 |
| `16_conway.py` | 康威生命游戏 | 细胞自动机 |
| `17_tetris.py` | 俄罗斯方块 | 完整游戏逻辑 |
| `18_magic_tower.py` | 魔塔 RPG | Tilemap + 场景管理 |

```bash
ezgame list          # 列出所有示例
ezgame run snake     # 按关键词运行
python examples/01_hello.py  # 直接运行
```


## API 参考

Python 接口遵循 `snake_case` 命名，与 C++ 的 `PascalCase` 一一对应。

### 窗口与主循环

| 方法 | 说明 |
|-|-|
| `open(w, h, title, center, resizable)` | 创建窗口；`w/h` 为 framebuffer 逻辑尺寸 |
| `is_closed()` | 窗口是否已关闭 |
| `update()` | 刷新画面并处理输入，每帧调用一次 |
| `wait_frame(fps)` | 帧率控制 |
| `get_delta_time()` | 帧间隔（秒） |
| `get_fps()` | 当前帧率 |
| `get_time()` | 运行总时间（秒） |
| `get_width()` / `get_height()` | framebuffer 逻辑尺寸 |
| `win_resize(w, h)` | 设置窗口客户区尺寸 |
| `set_maximized(maximized)` | 最大化或还原可缩放窗口 |
| `set_title(title)` | 修改窗口标题 |
| `show_fps(show)` | 标题栏显示实时 FPS |
| `show_mouse(show)` | 显示或隐藏鼠标光标 |
| `aspect_lock(lock, color)` | 锁定长宽比，黑边填充指定颜色 |
| `show_message(text, title, buttons)` | 弹出消息框 |

### 绘图

| 方法 | 说明 |
|-|-|
| `clear(color)` | 清屏 |
| `set_pixel(x, y, color)` | 画点（支持 Alpha 混合） |
| `get_pixel(x, y)` | 读点 |
| `set_clip(x, y, w, h)` | 设置裁剪矩形 |
| `clear_clip()` | 清除裁剪，恢复整屏 |
| `get_clip()` | 获取当前裁剪矩形 `(x, y, w, h)` |
| `get_clip_x()` / `get_clip_y()` / `get_clip_w()` / `get_clip_h()` | 获取裁剪矩形各分量 |
| `screenshot(filename)` | 保存当前帧为 BMP 文件 |
| `draw_line(x1, y1, x2, y2, color)` | 画线 |
| `draw_rect(x, y, w, h, color)` | 矩形边框 |
| `fill_rect(x, y, w, h, color)` | 填充矩形 |
| `draw_circle(cx, cy, r, color)` | 圆形边框 |
| `fill_circle(cx, cy, r, color)` | 填充圆 |
| `draw_ellipse(cx, cy, rx, ry, color)` | 椭圆边框 |
| `fill_ellipse(cx, cy, rx, ry, color)` | 填充椭圆 |
| `draw_triangle(x1, y1, x2, y2, x3, y3, color)` | 三角形边框 |
| `fill_triangle(x1, y1, x2, y2, x3, y3, color)` | 填充三角形 |

### 文字

| 方法 | 说明 |
|-|-|
| `draw_text(x, y, text, color)` | 内置 8x8 字体绘制文字 |
| `draw_number(x, y, number, color)` | 绘制整数 |
| `draw_text_scale(x, y, text, color, w, h)` | 缩放文字（每字符 w×h 像素） |
| `draw_printf(x, y, color, text)` | 格式化输出（Python 中用 f-string） |
| `draw_printf_scale(x, y, color, w, h, text)` | 缩放格式化输出 |
| `draw_text_font(x, y, text, color, size)` | 可缩放字体绘制（支持 UTF-8） |
| `draw_text_font(x, y, text, color, font, size)` | 指定字体绘制 |
| `get_text_width_font(...)` / `get_text_height_font(...)` | 测量文字尺寸 |

### 精灵系统

| 方法 | 说明 |
|-|-|
| `create_sprite(w, h)` | 创建空白精灵，返回 ID |
| `load_sprite(filename)` | 加载图片精灵（PNG/JPG/BMP/GIF/TIFF） |
| `load_sprite_bmp(filename)` | 从 BMP 加载精灵 |
| `free_sprite(id)` | 释放精灵 |
| `draw_sprite(id, x, y)` | 绘制精灵（不透明快路径） |
| `draw_sprite_ex(id, x, y, flags)` | 带翻转/透明/Alpha 混合绘制 |
| `draw_sprite_region(id, x, y, sx, sy, sw, sh)` | 绘制精灵子区域 |
| `draw_sprite_region_ex(id, x, y, sx, sy, sw, sh, flags)` | 带标志绘制精灵子区域 |
| `draw_sprite_scaled(id, x, y, w, h, flags)` | 缩放绘制 |
| `draw_sprite_rotated(id, cx, cy, angle, flags)` | 旋转绘制 |
| `draw_sprite_frame(id, x, y, fw, fh, index, flags)` | 绘制 sprite sheet 帧 |
| `draw_sprite_frame_scaled(...)` | 缩放绘制帧 |
| `draw_sprite_frame_rotated(...)` | 旋转绘制帧 |
| `set_sprite_pixel(id, x, y, color)` | 修改精灵像素 |
| `get_sprite_pixel(id, x, y)` | 读取精灵像素 |
| `get_sprite_width(id)` / `get_sprite_height(id)` | 读取精灵尺寸 |
| `set_sprite_color_key(id, color)` | 设置 Color Key |
| `get_sprite_color_key(id)` | 读取 Color Key |

精灵标志：`SPRITE_FLIP_H`（水平翻转）、`SPRITE_FLIP_V`（垂直翻转）、`SPRITE_COLORKEY`（Color Key 透明）、`SPRITE_ALPHA`（Alpha 混合）

> **注意**：`draw_sprite(id, x, y)` 默认走不透明快路径。如果素材需要透明，请显式传入 `SPRITE_COLORKEY` 或 `SPRITE_ALPHA` 标志。

### 输入

| 方法 | 说明 |
|-|-|
| `is_key_down(key)` | 按键是否按住 |
| `is_key_pressed(key)` | 按键是否刚按下（单次触发） |
| `is_key_released(key)` | 按键是否刚松开（单次触发） |
| `get_mouse_x()` / `get_mouse_y()` | 鼠标位置（自动映射到 framebuffer 坐标） |
| `is_mouse_down(button)` | 鼠标按键是否按下 |
| `is_mouse_pressed(button)` | 鼠标按键是否刚按下（单次触发） |
| `is_mouse_released(button)` | 鼠标按键是否刚松开（单次触发） |
| `get_mouse_wheel_delta()` | 滚轮增量 |
| `is_active()` | 窗口是否处于激活状态 |

### 声音

| 方法 | 说明 |
|-|-|
| `play_wav(filename, repeat, volume)` | 播放 WAV 音效，返回通道 ID |
| `play_beep(freq, duration, repeat, volume)` | 蜂鸣器，返回通道 ID |
| `stop_wav(channel)` | 停止指定通道 |
| `is_playing(channel)` | 查询通道是否播放中 |
| `set_volume(channel, volume)` | 设置通道音量（0-1000） |
| `stop_all()` | 停止所有音效 |
| `set_master_volume(volume)` | 设置主音量（0-1000） |
| `get_master_volume()` | 获取主音量 |
| `play_music(filename, loop)` | 播放背景音乐（MP3/MIDI/WAV） |
| `stop_music()` | 停止背景音乐 |
| `is_music_playing()` | 音乐是否播放中 |

### Tilemap 瓦片地图

| 方法 | 说明 |
|-|-|
| `create_tilemap(cols, rows, tile_size, tileset_id)` | 创建瓦片地图 |
| `save_tilemap(filename, map_id)` | 保存到 `.glm` 文件 |
| `load_tilemap(filename, tileset_id)` | 从 `.glm` 文件加载 |
| `free_tilemap(map_id)` | 释放地图 |
| `set_tile(map_id, col, row, tile_id)` | 设置瓦片（-1=空） |
| `get_tile(map_id, col, row)` | 读取瓦片 |
| `get_tilemap_cols(map_id)` / `get_tilemap_rows(map_id)` | 读取地图尺寸 |
| `get_tile_size(map_id)` | 读取瓦片尺寸 |
| `world_to_tile_col(map_id, x)` / `world_to_tile_row(map_id, y)` | 像素坐标转瓦片坐标 |
| `get_tile_at_pixel(map_id, x, y)` | 按像素位置读取瓦片 |
| `fill_tile_rect(map_id, col, row, cols, rows, tile_id)` | 批量填充矩形区域 |
| `clear_tilemap(map_id, tile_id)` | 清空地图 |
| `draw_tilemap(map_id, x, y, flags)` | 绘制地图（传 `-cameraX, -cameraY` 实现卷轴） |

### 场景管理

| 方法 | 说明 |
|-|-|
| `set_scene(scene)` | 切换场景（下一帧生效） |
| `get_scene()` | 获取当前场景 |
| `is_scene_changed()` | 本帧是否刚进入新场景 |
| `get_previous_scene()` | 获取切换前的场景 |

### UI 控件

所有 UI 控件均为立即模式（Immediate Mode），每帧调用一次即可自动绘制和响应交互。

**基础控件：**

| 方法 | 说明 |
|-|-|
| `button(x, y, w, h, text, color)` | 按钮，点击返回 `True` |
| `checkbox(x, y, text, checked)` | 复选框，返回 `(triggered, checked)` |
| `radio_box(x, y, text, value, index)` | 单选框，返回 `(triggered, value)` |
| `toggle_button(x, y, w, h, text, toggled, color)` | 开关按钮，返回 `(triggered, toggled)` |
| `slider(x, y, w, value, min_val, max_val)` | 水平滑块，返回 `(changed, value)` |
| `progress_bar(x, y, w, h, value, max_val, color)` | 进度条 |
| `spinner(x, y, w, value, min_val, max_val, step)` | 数字微调器，返回 `(changed, value)` |
| `knob(x, y, size, value, min_val, max_val)` | 旋钮控件，返回 `(changed, value)` |
| `separator(x, y, w)` | 水平分隔线 |
| `v_separator(x, y, h)` | 垂直分隔线 |
| `label(x, y, w, h, text, bg_color, text_color)` | 居中文字标签 |

**输入与选择：**

| 方法 | 说明 |
|-|-|
| `text_input(x, y, w, buffer, focused)` | 文本输入框，返回 `(changed, text, focused)` |
| `dropdown(x, y, w, items, selected_index, open)` | 下拉选择框，返回 `(changed, selected_index, open)` |
| `list_box(x, y, w, h, items, selected_index, scroll_offset)` | 可滚动列表框，返回 `(changed, selected_index, scroll_offset)` |
| `color_picker(x, y, colors, selected_index)` | 颜色选择器，返回 `(changed, selected_index)` |

**导航与布局：**

| 方法 | 说明 |
|-|-|
| `tab_bar(x, y, w, tabs, selected_tab)` | 标签栏，返回 `(changed, selected_tab)` |
| `tab_panel(x, y, w, h, tabs, selected_tab)` | 标签面板，返回 `(active_tab, cx, cy, cw, ch)` |
| `collapsible(x, y, w, title, open)` | 可折叠区域，返回 `(triggered, open)` |
| `menu(x, y, items, open)` | 弹出菜单，返回 `(selected_index, open)` |

**其他：** `tooltip(x, y, text)` 工具提示 · `image_button(x, y, w, h, sprite_id, color)` 图片按钮

> **提示**：`tab_panel` 返回的 `(cx, cy, cw, ch)` 是内容区域坐标，可直接用于放置子控件。

### 网格辅助

| 方法 | 说明 |
|-|-|
| `draw_grid(x, y, rows, cols, cell_size, color)` | 绘制网格 |
| `fill_cell(grid_x, grid_y, row, col, cell_size, color)` | 填充网格单元格 |

### 存档读写（静态方法）

| 方法 | 说明 |
|-|-|
| `GameLib.save_int(filename, key, value)` | 保存整数 |
| `GameLib.save_float(filename, key, value)` | 保存浮点数 |
| `GameLib.save_string(filename, key, value)` | 保存字符串 |
| `GameLib.load_int(filename, key, default)` | 读取整数 |
| `GameLib.load_float(filename, key, default)` | 读取浮点数 |
| `GameLib.load_string(filename, key, default)` | 读取字符串 |
| `GameLib.has_save_key(filename, key)` | 判断 key 是否存在 |
| `GameLib.delete_save_key(filename, key)` | 删除指定 key |
| `GameLib.delete_save(filename)` | 删除整个存档 |

### 工具方法（静态方法）

| 方法 | 说明 |
|-|-|
| `GameLib.random(min, max)` | 随机数 `[min, max]` |
| `GameLib.rect_overlap(x1, y1, w1, h1, x2, y2, w2, h2)` | 矩形碰撞检测 |
| `GameLib.circle_overlap(cx1, cy1, r1, cx2, cy2, r2)` | 圆形碰撞检测 |
| `GameLib.point_in_rect(px, py, x, y, w, h)` | 点在矩形内 |
| `GameLib.distance(x1, y1, x2, y2)` | 两点距离 |

### 颜色常量

```
COLOR_BLACK    COLOR_WHITE     COLOR_RED       COLOR_GREEN     COLOR_BLUE
COLOR_YELLOW   COLOR_CYAN      COLOR_MAGENTA   COLOR_ORANGE    COLOR_PINK
COLOR_PURPLE   COLOR_GRAY      COLOR_DARK_GRAY COLOR_LIGHT_GRAY
COLOR_DARK_RED COLOR_DARK_GREEN COLOR_DARK_BLUE COLOR_SKY_BLUE
COLOR_BROWN    COLOR_GOLD      COLOR_TRANSPARENT
```

自定义颜色：`COLOR_RGB(r, g, b)` 或 `COLOR_ARGB(a, r, g, b)`

分量提取：`COLOR_GET_A(c)` / `COLOR_GET_R(c)` / `COLOR_GET_G(c)` / `COLOR_GET_B(c)`

### 工具函数

| 函数 | 说明 |
|-|-|
| `get_respath(*parts)` | 获取包资源目录下的绝对路径（POSIX 格式） |
| `get_asset_path(filename)` | 获取 `clib/assets/` 下文件的绝对路径（POSIX 格式） |
| `clamp(value, lo, hi)` | 将值限制在 `[lo, hi]` 范围内 |
| `safe_dt(game, max_dt)` | 获取帧间隔，上限截断防止跳帧（默认上限 0.05s） |
| `draw_checkerboard(game, x, y, w, h, cell)` | 绘制棋盘格图案 |
| `draw_panel(game, x, y, w, h, title)` | 绘制带标题栏的面板 |


## 从源码构建

**前置要求：** Python 3.9+、C++14 编译器（MSVC 2015+ / GCC 4.9+ / Clang）、CMake 3.15+

```bash
git clone --recursive <repo-url> && cd pyezgame
pip install .

# 或开发模式
pip install -e . --no-build-isolation
```

Linux / macOS 需安装 SDL2 开发包：

```bash
# Ubuntu / Debian
sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-ttf-dev libsdl2-mixer-dev

# macOS
brew install sdl2 sdl2_image sdl2_ttf sdl2_mixer
```


## C++ 与 Python 对照

| C++ (GameLib) | Python (pyezgame) |
|-|-|
| `game.Open(640, 480, "Title", true)` | `game.open(640, 480, "Title", True)` |
| `game.Clear(COLOR_BLACK)` | `game.clear(COLOR_BLACK)` |
| `game.FillCircle(x, y, r, color)` | `game.fill_circle(x, y, r, color)` |
| `game.DrawText(x, y, "hi", color)` | `game.draw_text(x, y, "hi", color)` |
| `game.IsKeyDown(KEY_LEFT)` | `game.is_key_down(KEY_LEFT)` |
| `game.DrawPrintf(x, y, c, "Score: %d", s)` | `game.draw_printf(x, y, c, f"Score: {s}")` |
| `GameLib::Random(0, 100)` | `GameLib.random(0, 100)` |

> C++ 的 `Checkbox(x, y, text, &checked)` 通过指针修改值；Python 返回 `(triggered, checked)` 元组，需手动更新状态变量。


## 致谢

- [GameLib](https://github.com/skywind3000/GameLib) — 底层 C++ 游戏库，单头文件，零依赖
- [pybind11](https://github.com/pybind/pybind11) — C++ / Python 互操作绑定
- [scikit-build-core](https://github.com/scikit-build/scikit-build-core) — Python C 扩展构建系统


## 协议

MIT License
