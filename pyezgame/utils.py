from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._pyezgame import GameLib

ROOT_PATH = Path(__file__).parent


def get_respath(*parts: str | Path) -> str:
    """Get the absolute path to a resource (POSIX format).

    Args:
        *parts: Path components relative to the package root.

    Returns:
        str: The absolute POSIX path to the resource.
    """
    return (ROOT_PATH / Path(*parts)).as_posix()


def get_asset_path(filename: str) -> str:
    """Get the absolute POSIX path to a file inside clib/assets/.

    Args:
        filename: Asset filename (e.g. ``"coin.png"``).

    Returns:
        str: The absolute POSIX path to the asset file.
    """
    return (ROOT_PATH.parent / "clib" / "assets" / filename).as_posix()


def clamp(value: int, lo: int, hi: int) -> int:
    """Clamp *value* into ``[lo, hi]``.

    Args:
        value: The integer to clamp.
        lo: Lower bound (inclusive).
        hi: Upper bound (inclusive).

    Returns:
        int: The clamped value.
    """
    return max(lo, min(hi, value))


def safe_dt(game: GameLib, max_dt: float = 0.05) -> float:
    """Return ``game.get_delta_time()`` capped at *max_dt* seconds.

    Prevents physics explosions after long pauses or frame drops.

    Args:
        game: The GameLib instance.
        max_dt: Maximum allowed delta time (default 0.05s = 20 FPS minimum).

    Returns:
        float: The capped delta time in seconds.
    """
    dt = game.get_delta_time()
    return min(dt, max_dt)


def draw_checkerboard(
    game: GameLib,
    x: int,
    y: int,
    w: int,
    h: int,
    cell: int,
) -> None:
    """Draw a checkerboard pattern inside the rectangle (*x*, *y*, *w*, *h*).

    Uses ``COLOR_LIGHT_GRAY`` and ``COLOR_WHITE`` for the two alternating colors.

    Args:
        game: The GameLib instance.
        x: Left edge of the pattern.
        y: Top edge of the pattern.
        w: Total width in pixels.
        h: Total height in pixels.
        cell: Size of each checkerboard cell in pixels.
    """
    from ._pyezgame import COLOR_LIGHT_GRAY, COLOR_WHITE

    cols = (w + cell - 1) // cell
    rows = (h + cell - 1) // cell
    for r in range(rows):
        for c in range(cols):
            color = COLOR_LIGHT_GRAY if (r + c) % 2 == 0 else COLOR_WHITE
            cx = x + c * cell
            cy = y + r * cell
            cw = min(cell, x + w - cx)
            ch = min(cell, y + h - cy)
            game.fill_rect(cx, cy, cw, ch, color)


def draw_panel(
    game: GameLib,
    x: int,
    y: int,
    w: int,
    h: int,
    title: str,
) -> None:
    """Draw a panel with a title bar.

    The title bar is 20 pixels tall with a ``COLOR_DARK_BLUE`` background
    and ``COLOR_WHITE`` text.  The body has a ``COLOR_LIGHT_GRAY`` background
    with a ``COLOR_DARK_GRAY`` border.

    Args:
        game: The GameLib instance.
        x: Left edge of the panel.
        y: Top edge of the panel.
        w: Panel width in pixels.
        h: Panel height in pixels (including title bar).
        title: Title text displayed in the title bar.
    """
    from ._pyezgame import (
        COLOR_DARK_BLUE,
        COLOR_DARK_GRAY,
        COLOR_LIGHT_GRAY,
        COLOR_WHITE,
    )

    title_h = 20
    # body
    game.fill_rect(x, y, w, h, COLOR_LIGHT_GRAY)
    game.draw_rect(x, y, w, h, COLOR_DARK_GRAY)
    # title bar
    game.fill_rect(x, y, w, title_h, COLOR_DARK_BLUE)
    game.draw_text(x + 4, y + 6, title, COLOR_WHITE)
