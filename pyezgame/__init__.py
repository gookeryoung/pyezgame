"""
pyezgame - Python bindings for GameLib

A beginner-friendly game development library with simple API for
window creation, graphics, sprites, sound, input, and more.
"""

from ._pyezgame import *  # noqa: F401, F403
from ._pyezgame import GameLib

__version__ = "0.1.2"
__all__ = ["GameLib"]
