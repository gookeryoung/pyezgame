"""
pyezgame - Python bindings for GameLib

A beginner-friendly game development library with simple API for
window creation, graphics, sprites, sound, input, and more.
"""

from ._pyezgame import *  # noqa: F403
from ._pyezgame import GameLib
from .utils import get_respath

__version__ = "0.2.7"
__all__ = ["GameLib", "get_respath"]
