"""
pyezgame - Python bindings for GameLib

A beginner-friendly game development library with simple API for
window creation, graphics, sprites, sound, input, and more.
"""

from __future__ import annotations

from pathlib import Path
from typing import overload

__version__: str

# ===========================================================================
# Color Constants (ARGB format: 0xAARRGGBB)
# ===========================================================================
COLOR_BLACK: int
COLOR_WHITE: int
COLOR_RED: int
COLOR_GREEN: int
COLOR_BLUE: int
COLOR_YELLOW: int
COLOR_CYAN: int
COLOR_MAGENTA: int
COLOR_ORANGE: int
COLOR_PINK: int
COLOR_PURPLE: int
COLOR_GRAY: int
COLOR_DARK_GRAY: int
COLOR_LIGHT_GRAY: int
COLOR_DARK_RED: int
COLOR_DARK_GREEN: int
COLOR_DARK_BLUE: int
COLOR_SKY_BLUE: int
COLOR_BROWN: int
COLOR_GOLD: int
COLOR_TRANSPARENT: int
COLORKEY_DEFAULT: int

# ===========================================================================
# Color Helper Functions
# ===========================================================================
def COLOR_RGB(r: int, g: int, b: int) -> int:
    """Create an opaque ARGB color from R, G, B components (each 0-255)."""
    ...

def COLOR_ARGB(a: int, r: int, g: int, b: int) -> int:
    """Create an ARGB color from A, R, G, B components (each 0-255)."""
    ...

def COLOR_GET_A(c: int) -> int:
    """Extract alpha component from an ARGB color."""
    ...

def COLOR_GET_R(c: int) -> int:
    """Extract red component from an ARGB color."""
    ...

def COLOR_GET_G(c: int) -> int:
    """Extract green component from an ARGB color."""
    ...

def COLOR_GET_B(c: int) -> int:
    """Extract blue component from an ARGB color."""
    ...

# ===========================================================================
# Keyboard Constants
# ===========================================================================
KEY_LEFT: int
KEY_RIGHT: int
KEY_UP: int
KEY_DOWN: int
KEY_SPACE: int
KEY_ENTER: int
KEY_ESCAPE: int
KEY_TAB: int
KEY_SHIFT: int
KEY_CONTROL: int
KEY_BACK: int

KEY_A: int
KEY_B: int
KEY_C: int
KEY_D: int
KEY_E: int
KEY_F: int
KEY_G: int
KEY_H: int
KEY_I: int
KEY_J: int
KEY_K: int
KEY_L: int
KEY_M: int
KEY_N: int
KEY_O: int
KEY_P: int
KEY_Q: int
KEY_R: int
KEY_S: int
KEY_T: int
KEY_U: int
KEY_V: int
KEY_W: int
KEY_X: int
KEY_Y: int
KEY_Z: int

KEY_0: int
KEY_1: int
KEY_2: int
KEY_3: int
KEY_4: int
KEY_5: int
KEY_6: int
KEY_7: int
KEY_8: int
KEY_9: int

KEY_F1: int
KEY_F2: int
KEY_F3: int
KEY_F4: int
KEY_F5: int
KEY_F6: int
KEY_F7: int
KEY_F8: int
KEY_F9: int
KEY_F10: int
KEY_F11: int
KEY_F12: int
KEY_ADD: int
KEY_SUBTRACT: int

# ===========================================================================
# Mouse Button Constants
# ===========================================================================
MOUSE_LEFT: int
MOUSE_RIGHT: int
MOUSE_MIDDLE: int

# ===========================================================================
# Message Box Constants
# ===========================================================================
MESSAGEBOX_OK: int
MESSAGEBOX_YESNO: int
MESSAGEBOX_RESULT_OK: int
MESSAGEBOX_RESULT_YES: int
MESSAGEBOX_RESULT_NO: int

# ===========================================================================
# Sprite Flag Constants
# ===========================================================================
SPRITE_FLIP_H: int
SPRITE_FLIP_V: int
SPRITE_COLORKEY: int
SPRITE_ALPHA: int

# ===========================================================================
# GameLib Class
# ===========================================================================
class GameLib:
    """Main game library class providing window, graphics, input, sound, and more."""

    def __init__(self) -> None: ...

    # ---- Window and Main Loop ----

    def open(
        self,
        width: int,
        height: int,
        title: str,
        center: bool = False,
        resizable: bool = False,
    ) -> int:
        """Create window and initialize framebuffer.

        Returns 0 on success, negative error code on failure.
        """
        ...

    def is_closed(self) -> bool:
        """Check if the window has been closed."""
        ...

    def update(self) -> None:
        """Refresh the display and process input. Call once per frame."""
        ...

    def wait_frame(self, fps: int) -> None:
        """Frame rate control. Blocks until the next frame boundary."""
        ...

    def get_delta_time(self) -> float:
        """Get time elapsed since last frame (seconds)."""
        ...

    def get_fps(self) -> float:
        """Get current frames per second (updated once per second)."""
        ...

    def get_time(self) -> float:
        """Get total running time since open() (seconds)."""
        ...

    def get_width(self) -> int:
        """Get framebuffer logical width (pixels)."""
        ...

    def get_height(self) -> int:
        """Get framebuffer logical height (pixels)."""
        ...

    def win_resize(self, width: int, height: int) -> None:
        """Set window client area size (does not change framebuffer size)."""
        ...

    def set_maximized(self, maximized: bool) -> None:
        """Maximize or restore a resizable window."""
        ...

    def set_title(self, title: str) -> None:
        """Set window title (supports UTF-8)."""
        ...

    def show_fps(self, show: bool) -> None:
        """Show or hide real-time FPS in the title bar."""
        ...

    def show_mouse(self, show: bool) -> None:
        """Show or hide the mouse cursor inside the window."""
        ...

    def aspect_lock(self, lock: bool, color: int = COLOR_BLACK) -> None:
        """Lock framebuffer aspect ratio during resize; fill letterbox with color."""
        ...

    def show_message(
        self,
        text: str,
        title: str | None = None,
        buttons: int = MESSAGEBOX_OK,
    ) -> int:
        """Show a message box. Returns MESSAGEBOX_RESULT_OK/YES/NO."""
        ...

    # ---- Framebuffer ----

    def clear(self, color: int = COLOR_BLACK) -> None:
        """Fill the current clip rect with the given color (no alpha blending)."""
        ...

    def set_pixel(self, x: int, y: int, color: int) -> None:
        """Set a pixel color (supports alpha blending)."""
        ...

    def get_pixel(self, x: int, y: int) -> int:
        """Get a pixel's ARGB color. Returns 0 if out of bounds."""
        ...

    def set_clip(self, x: int, y: int, w: int, h: int) -> None:
        """Set clip rectangle (auto-intersected with screen bounds)."""
        ...

    def clear_clip(self) -> None:
        """Clear clip rectangle, restoring full screen visibility."""
        ...

    def get_clip(self) -> tuple[int, int, int, int]:
        """Get current effective clip rectangle as (x, y, w, h)."""
        ...

    def get_clip_x(self) -> int:
        """Get current clip rectangle X coordinate."""
        ...

    def get_clip_y(self) -> int:
        """Get current clip rectangle Y coordinate."""
        ...

    def get_clip_w(self) -> int:
        """Get current clip rectangle width."""
        ...

    def get_clip_h(self) -> int:
        """Get current clip rectangle height."""
        ...

    def screenshot(self, filename: str) -> None:
        """Save framebuffer as a 24-bit BMP file (UTF-8 path)."""
        ...

    # ---- Drawing ----

    def draw_line(self, x1: int, y1: int, x2: int, y2: int, color: int) -> None:
        """Draw a line using Bresenham's algorithm (supports alpha blending)."""
        ...

    def draw_rect(self, x: int, y: int, w: int, h: int, color: int) -> None:
        """Draw a rectangle outline (supports alpha blending)."""
        ...

    def fill_rect(self, x: int, y: int, w: int, h: int, color: int) -> None:
        """Fill a rectangle (supports alpha blending)."""
        ...

    def draw_circle(self, cx: int, cy: int, r: int, color: int) -> None:
        """Draw a circle outline (supports alpha blending)."""
        ...

    def fill_circle(self, cx: int, cy: int, r: int, color: int) -> None:
        """Fill a circle (supports alpha blending)."""
        ...

    def draw_ellipse(self, cx: int, cy: int, rx: int, ry: int, color: int) -> None:
        """Draw an ellipse outline (supports alpha blending)."""
        ...

    def fill_ellipse(self, cx: int, cy: int, rx: int, ry: int, color: int) -> None:
        """Fill an ellipse (supports alpha blending)."""
        ...

    def draw_triangle(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        x3: int,
        y3: int,
        color: int,
    ) -> None:
        """Draw a triangle outline (supports alpha blending)."""
        ...

    def fill_triangle(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        x3: int,
        y3: int,
        color: int,
    ) -> None:
        """Fill a triangle using scanline algorithm (supports alpha blending)."""
        ...

    # ---- Text Rendering (built-in 8x8 font) ----

    def draw_text(self, x: int, y: int, text: str, color: int) -> None:
        """Draw text using built-in 8x8 bitmap font (ASCII 32-126)."""
        ...

    def draw_number(self, x: int, y: int, number: int, color: int) -> None:
        """Draw an integer as text using built-in 8x8 font."""
        ...

    def draw_text_scale(
        self,
        x: int,
        y: int,
        text: str,
        color: int,
        w: int,
        h: int,
    ) -> None:
        """Draw text with each character scaled to w x h pixels (max 1024)."""
        ...

    def draw_printf(self, x: int, y: int, color: int, text: str) -> None:
        """Draw pre-formatted text at position using built-in 8x8 font.

        In Python, use f-strings for formatting instead of C printf format strings.
        Example: game.draw_printf(10, 10, COLOR_WHITE, f"Score: {score}")
        """
        ...

    def draw_printf_scale(
        self,
        x: int,
        y: int,
        color: int,
        w: int,
        h: int,
        text: str,
    ) -> None:
        """Draw pre-formatted text with scaling.

        In Python, use f-strings for formatting.
        """
        ...

    # ---- Font Text Rendering (scalable fonts, Unicode) ----

    @overload
    def draw_text_font(
        self,
        x: int,
        y: int,
        text: str,
        color: int,
        font_name: str,
        font_size: int,
    ) -> None:
        """Draw text with a named font at the given size (supports UTF-8)."""
        ...

    @overload
    def draw_text_font(
        self,
        x: int,
        y: int,
        text: str,
        color: int,
        font_size: int,
    ) -> None:
        """Draw text with the default font at the given size (supports UTF-8)."""
        ...

    @overload
    def get_text_width_font(self, text: str, font_name: str, font_size: int) -> int:
        """Measure text width with a named font."""
        ...

    @overload
    def get_text_width_font(self, text: str, font_size: int) -> int:
        """Measure text width with the default font."""
        ...

    @overload
    def get_text_height_font(self, text: str, font_name: str, font_size: int) -> int:
        """Measure text height with a named font."""
        ...

    @overload
    def get_text_height_font(self, text: str, font_size: int) -> int:
        """Measure text height with the default font."""
        ...

    @overload
    def draw_printf_font(
        self,
        x: int,
        y: int,
        color: int,
        font_name: str,
        font_size: int,
        text: str,
    ) -> None:
        """Draw pre-formatted text with a named font.

        In Python, use f-strings for formatting.
        """
        ...

    @overload
    def draw_printf_font(
        self,
        x: int,
        y: int,
        color: int,
        font_size: int,
        text: str,
    ) -> None:
        """Draw pre-formatted text with the default font.

        In Python, use f-strings for formatting.
        """
        ...

    # ---- Sprite System ----

    def create_sprite(self, width: int, height: int) -> int:
        """Create a blank sprite. Returns sprite ID, or -1 on failure."""
        ...

    def load_sprite(self, filename: str) -> int:
        """Load sprite from image file (PNG/JPG/BMP/GIF/TIFF). Returns sprite ID, or -1 on failure."""
        ...

    def load_sprite_bmp(self, filename: str) -> int:
        """Load sprite from BMP file (8/24/32-bit). Returns sprite ID, or -1 on failure."""
        ...

    def free_sprite(self, id: int) -> None:
        """Free a sprite by ID."""
        ...

    def draw_sprite(self, id: int, x: int, y: int) -> None:
        """Draw sprite at position (opaque fast path)."""
        ...

    def draw_sprite_ex(self, id: int, x: int, y: int, flags: int) -> None:
        """Draw sprite with flags (SPRITE_FLIP_H/V, SPRITE_COLORKEY, SPRITE_ALPHA)."""
        ...

    def draw_sprite_region(
        self,
        id: int,
        x: int,
        y: int,
        sx: int,
        sy: int,
        sw: int,
        sh: int,
    ) -> None:
        """Draw a sub-region of a sprite."""
        ...

    def draw_sprite_region_ex(
        self,
        id: int,
        x: int,
        y: int,
        sx: int,
        sy: int,
        sw: int,
        sh: int,
        flags: int = 0,
    ) -> None:
        """Draw a sub-region of a sprite with flags."""
        ...

    def draw_sprite_scaled(
        self,
        id: int,
        x: int,
        y: int,
        w: int,
        h: int,
        flags: int = 0,
    ) -> None:
        """Draw sprite scaled to target size (nearest-neighbor)."""
        ...

    def draw_sprite_rotated(
        self,
        id: int,
        cx: int,
        cy: int,
        angle_deg: float,
        flags: int = 0,
    ) -> None:
        """Draw sprite rotated around center point (angle_deg > 0 = clockwise)."""
        ...

    def draw_sprite_frame(
        self,
        id: int,
        x: int,
        y: int,
        frame_w: int,
        frame_h: int,
        frame_index: int,
        flags: int = 0,
    ) -> None:
        """Draw a single frame from a sprite sheet."""
        ...

    def draw_sprite_frame_scaled(
        self,
        id: int,
        x: int,
        y: int,
        frame_w: int,
        frame_h: int,
        frame_index: int,
        w: int,
        h: int,
        flags: int = 0,
    ) -> None:
        """Draw a single frame from a sprite sheet, scaled to target size."""
        ...

    def draw_sprite_frame_rotated(
        self,
        id: int,
        cx: int,
        cy: int,
        frame_w: int,
        frame_h: int,
        frame_index: int,
        angle_deg: float,
        flags: int = 0,
    ) -> None:
        """Draw a single frame from a sprite sheet, rotated around center."""
        ...

    def set_sprite_pixel(self, id: int, x: int, y: int, color: int) -> None:
        """Set a pixel on a sprite."""
        ...

    def get_sprite_pixel(self, id: int, x: int, y: int) -> int:
        """Get a pixel's ARGB color from a sprite."""
        ...

    def get_sprite_width(self, id: int) -> int:
        """Get sprite width in pixels. Returns 0 for invalid ID."""
        ...

    def get_sprite_height(self, id: int) -> int:
        """Get sprite height in pixels. Returns 0 for invalid ID."""
        ...

    def set_sprite_color_key(self, id: int, color: int) -> None:
        """Set the color key for a sprite (used with SPRITE_COLORKEY flag)."""
        ...

    def get_sprite_color_key(self, id: int) -> int:
        """Get the color key of a sprite (default: COLORKEY_DEFAULT = magenta)."""
        ...

    # ---- Tilemap System ----

    def create_tilemap(self, cols: int, rows: int, tile_size: int, tileset_id: int) -> int:
        """Create a tilemap. Returns map ID, or -1 on failure."""
        ...

    def save_tilemap(self, filename: str, map_id: int) -> bool:
        """Save tilemap to .glm file. Returns True on success."""
        ...

    def load_tilemap(self, filename: str, tileset_id: int) -> int:
        """Load tilemap from .glm file. Returns map ID, or -1 on failure."""
        ...

    def free_tilemap(self, map_id: int) -> None:
        """Free a tilemap by ID."""
        ...

    def set_tile(self, map_id: int, col: int, row: int, tile_id: int) -> None:
        """Set a tile (-1 = empty, < -1 ignored)."""
        ...

    def get_tile(self, map_id: int, col: int, row: int) -> int:
        """Get tile ID at position. Returns -1 if out of bounds."""
        ...

    def get_tilemap_cols(self, map_id: int) -> int:
        """Get tilemap column count. Returns 0 for invalid ID."""
        ...

    def get_tilemap_rows(self, map_id: int) -> int:
        """Get tilemap row count. Returns 0 for invalid ID."""
        ...

    def get_tile_size(self, map_id: int) -> int:
        """Get tile size in pixels. Returns 0 for invalid ID."""
        ...

    def world_to_tile_col(self, map_id: int, x: int) -> int:
        """Convert pixel X to tile column (floor division)."""
        ...

    def world_to_tile_row(self, map_id: int, y: int) -> int:
        """Convert pixel Y to tile row (floor division)."""
        ...

    def get_tile_at_pixel(self, map_id: int, x: int, y: int) -> int:
        """Get tile ID at pixel position. Returns -1 if out of bounds or empty."""
        ...

    def fill_tile_rect(
        self,
        map_id: int,
        col: int,
        row: int,
        cols: int,
        rows: int,
        tile_id: int,
    ) -> None:
        """Fill a rectangular area of tiles (auto-clipped to map bounds)."""
        ...

    def clear_tilemap(self, map_id: int, tile_id: int = -1) -> None:
        """Clear entire tilemap to a single tile (-1 = empty)."""
        ...

    def draw_tilemap(self, map_id: int, x: int, y: int, flags: int = 0) -> None:
        """Draw tilemap at screen offset (pass -cameraX, -cameraY for scrolling)."""
        ...

    # ---- Grid Helpers ----

    def draw_grid(
        self,
        x: int,
        y: int,
        rows: int,
        cols: int,
        cell_size: int,
        color: int,
    ) -> None:
        """Draw a grid of cells."""
        ...

    def fill_cell(
        self,
        grid_x: int,
        grid_y: int,
        row: int,
        col: int,
        cell_size: int,
        color: int,
    ) -> None:
        """Fill a single grid cell (1px padding to avoid covering grid lines)."""
        ...

    # ---- Input ----

    def is_key_down(self, key: int) -> bool:
        """Check if a key is currently held down."""
        ...

    def is_key_pressed(self, key: int) -> bool:
        """Check if a key was just pressed this frame (edge trigger)."""
        ...

    def is_key_released(self, key: int) -> bool:
        """Check if a key was just released this frame (edge trigger)."""
        ...

    def get_mouse_x(self) -> int:
        """Get mouse X in framebuffer coordinates (accounts for window scaling)."""
        ...

    def get_mouse_y(self) -> int:
        """Get mouse Y in framebuffer coordinates (accounts for window scaling)."""
        ...

    def is_mouse_down(self, button: int) -> bool:
        """Check if a mouse button is currently held down."""
        ...

    def is_mouse_pressed(self, button: int) -> bool:
        """Check if a mouse button was just pressed this frame (edge trigger)."""
        ...

    def is_mouse_released(self, button: int) -> bool:
        """Check if a mouse button was just released this frame (edge trigger)."""
        ...

    def get_mouse_wheel_delta(self) -> int:
        """Get accumulated mouse wheel delta since last update() (120 per notch)."""
        ...

    def is_active(self) -> bool:
        """Check if the window is currently active (has focus)."""
        ...

    # ---- Sound ----

    def play_beep(
        self,
        frequency: int,
        duration: int,
        repeat: int = 1,
        volume: int = 1000,
    ) -> int:
        """Play a beep tone. Returns channel ID (>0), or negative on failure."""
        ...

    def play_wav(
        self,
        filename: str,
        repeat: int = 1,
        volume: int = 1000,
    ) -> int:
        """Play a WAV sound file. Returns channel ID (>0), or negative on failure."""
        ...

    def stop_wav(self, channel: int) -> int:
        """Stop a sound channel. Returns 0 on success, -1 if invalid channel."""
        ...

    def is_playing(self, channel: int) -> int:
        """Check if a channel is playing. Returns 1 if playing, 0 otherwise."""
        ...

    def set_volume(self, channel: int, volume: int) -> int:
        """Set channel volume (0-1000). Returns 0 on success, -1 if invalid channel."""
        ...

    def stop_all(self) -> None:
        """Stop all sound effects."""
        ...

    def set_master_volume(self, volume: int) -> int:
        """Set master volume (0-1000). Always returns 0."""
        ...

    def get_master_volume(self) -> int:
        """Get current master volume (0-1000)."""
        ...

    def play_music(self, filename: str, loop: bool = True) -> bool:
        """Play background music (MP3/MIDI/WAV). Returns True on success."""
        ...

    def stop_music(self) -> None:
        """Stop background music."""
        ...

    def is_music_playing(self) -> bool:
        """Check if background music is currently playing."""
        ...

    # ---- Scene Management ----

    def set_scene(self, scene: int) -> None:
        """Set scene to switch to on next update(). Use set_scene(get_scene()) to restart."""
        ...

    def get_scene(self) -> int:
        """Get current scene number (initial: 0)."""
        ...

    def is_scene_changed(self) -> bool:
        """Check if a new scene just started this frame (True on first frame of new scene)."""
        ...

    def get_previous_scene(self) -> int:
        """Get the scene number before the current one."""
        ...

    # ---- UI Helpers (built-in 8x8 font) ----

    def button(self, x: int, y: int, w: int, h: int, text: str, color: int) -> bool:
        """Draw an immediate-mode button. Returns True when clicked."""
        ...

    def checkbox(self, x: int, y: int, text: str, checked: bool) -> tuple[bool, bool]:
        """Draw an immediate-mode checkbox.

        Returns (triggered, checked) where triggered is True when state changed.
        """
        ...

    def radio_box(
        self,
        x: int,
        y: int,
        text: str,
        value: int,
        index: int,
    ) -> tuple[bool, int]:
        """Draw an immediate-mode radio button.

        Returns (triggered, value) where triggered is True when this item was selected.
        """
        ...

    def toggle_button(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        text: str,
        toggled: bool,
        color: int,
    ) -> tuple[bool, bool]:
        """Draw an immediate-mode toggle button.

        Returns (triggered, toggled) where triggered is True when state changed.
        """
        ...

    # ---- Static Methods: Save/Load ----

    @staticmethod
    def save_int(filename: str, key: str, value: int) -> bool:
        """Save an integer to a save file."""
        ...

    @staticmethod
    def save_float(filename: str, key: str, value: float) -> bool:
        """Save a float to a save file."""
        ...

    @staticmethod
    def save_string(filename: str, key: str, value: str) -> bool:
        """Save a string to a save file."""
        ...

    @staticmethod
    def load_int(filename: str, key: str, default_value: int = 0) -> int:
        """Load an integer from a save file. Returns default_value if not found."""
        ...

    @staticmethod
    def load_float(filename: str, key: str, default_value: float = 0.0) -> float:
        """Load a float from a save file. Returns default_value if not found."""
        ...

    @staticmethod
    def load_string(filename: str, key: str, default_value: str = "") -> str:
        """Load a string from a save file. Returns default_value if not found."""
        ...

    @staticmethod
    def has_save_key(filename: str, key: str) -> bool:
        """Check if a key exists in a save file."""
        ...

    @staticmethod
    def delete_save_key(filename: str, key: str) -> bool:
        """Delete a key from a save file."""
        ...

    @staticmethod
    def delete_save(filename: str) -> bool:
        """Delete an entire save file."""
        ...

    # ---- Static Methods: Utilities ----

    @staticmethod
    def random(min_val: int, max_val: int) -> int:
        """Return a random integer in [min_val, max_val]."""
        ...

    @staticmethod
    def rect_overlap(
        x1: int,
        y1: int,
        w1: int,
        h1: int,
        x2: int,
        y2: int,
        w2: int,
        h2: int,
    ) -> bool:
        """AABB rectangle collision detection."""
        ...

    @staticmethod
    def circle_overlap(
        cx1: int,
        cy1: int,
        r1: int,
        cx2: int,
        cy2: int,
        r2: int,
    ) -> bool:
        """Circle collision detection."""
        ...

    @staticmethod
    def point_in_rect(px: int, py: int, x: int, y: int, w: int, h: int) -> bool:
        """Check if a point is inside a rectangle."""
        ...

    @staticmethod
    def distance(x1: int, y1: int, x2: int, y2: int) -> float:
        """Calculate distance between two points."""
        ...

# ===========================================================================
# Utility Functions
# ===========================================================================

def get_respath(*parts: str | Path) -> str:
    """Get the absolute POSIX path to a package resource."""
    ...

def get_asset_path(filename: str) -> str:
    """Get the absolute POSIX path to a file inside clib/assets/."""
    ...

def clamp(value: int, lo: int, hi: int) -> int:
    """Clamp *value* into ``[lo, hi]``."""
    ...

def safe_dt(game: GameLib, max_dt: float = 0.05) -> float:
    """Return ``game.get_delta_time()`` capped at *max_dt* seconds."""
    ...

def draw_checkerboard(game: GameLib, x: int, y: int, w: int, h: int, cell: int) -> None:
    """Draw a checkerboard pattern inside the rectangle (*x*, *y*, *w*, *h*)."""
    ...

def draw_panel(game: GameLib, x: int, y: int, w: int, h: int, title: str) -> None:
    """Draw a panel with a title bar."""
    ...
