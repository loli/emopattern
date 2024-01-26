import importlib.resources

import yaml

from . import PromptGeneratorBase


class PromptGeneratorMirror(PromptGeneratorBase):
    def __init__(self):
        """Creates prompt based on randomly selected scenes and an LLM response utilizing the emotion reading."""
        with open(
            importlib.resources.files("emopattern.resources").joinpath("mirror.yaml"),
            "r",
        ) as f:
            self.config = yaml.safe_load(f)

    def get_prompt(self, emotions: dict[str, float], user_input: str | None = None):
        colorization = " and ".join([e for e, _ in emotions.items()])

        if user_input is None:
            user_input = self.DEFAULT_PROMPT

        return f"{user_input}, the image should spark {colorization}"
