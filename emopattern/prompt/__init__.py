"""
Prompt generation routines.

Each class stands for a schema to create prompts from the emotional readings as well as other inputs.
"""

from .base import PromptGeneratorBase
from .simple import PromptGeneratorSimple
from .mirror import PromptGeneratorMirror
from .emostring import PromptGeneratorEmostrings

__all__ = [
    "PromptGeneratorBase",
    "PromptGeneratorSimple",
    "PromptGeneratorMirror",
    "PromptGeneratorEmostrings",
]
