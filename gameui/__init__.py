"""
GameUI - Python bindings for GameLib

A beginner-friendly game development library with simple API for
window creation, graphics, sprites, sound, input, and more.
"""

from ._gameui import *  # noqa: F401, F403
from ._gameui import GameLib

__version__ = "0.1.0"
__all__ = ["GameLib"]
