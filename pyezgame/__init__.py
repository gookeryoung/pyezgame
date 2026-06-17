"""
pyezgame - Python bindings for GameLib

A beginner-friendly game development library with simple API for
window creation, graphics, sprites, sound, input, and more.
"""

from ._pyezgame import *  # noqa: F403
from ._pyezgame import GameLib
from .utils import (
    clamp,
    draw_checkerboard,
    draw_panel,
    get_asset_path,
    get_respath,
    safe_dt,
)

__version__ = "0.4.6"
__all__ = [
    "GameLib",
    "clamp",
    "draw_checkerboard",
    "draw_panel",
    "get_asset_path",
    "get_respath",
    "safe_dt",
]
