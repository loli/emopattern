import importlib.resources

import yaml

from . import PromptGeneratorBase


class PromptGeneratorMirror(PromptGeneratorBase):
    def __init__(self):
        with open(
            importlib.resources.files("emopattern.resources").joinpath("mirror.yaml"),
            "r",
        ) as f:
            self.config = yaml.safe_load(f)

    def get_prompt(self, emotions: dict[str, float], user_input: str | None = None):
        pass
