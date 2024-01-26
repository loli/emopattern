import time
import random
import importlib.resources

import yaml

from . import PromptGeneratorBase


class PromptGeneratorShuffle(PromptGeneratorBase):
    def __init__(self, promptfile: str = "shuffle.yaml", seconds: int = 30):
        """Creates prompt based by round-robin style shuffle along a list of scenes.

        Args:
            promptfile: Expected format is a YAML list of prompt to iterate through.
            seconds: Seconds between prompt changes
        """
        with importlib.resources.files("emopattern.resources").joinpath(
            promptfile
        ).open("rb") as f:
            self.config = yaml.safe_load(f)
        self.last_change = None
        self.idx = random.randint(0, len(self.config["prompts"]))
        self.seconds = seconds

    def get_prompt(self, emotions: dict[str, float], user_input: str | None = None):
        if self.last_change is None:
            self.last_change = time.time()

        if time.time() - self.last_change > self.seconds:
            self.idx += 1
            if self.idx >= len(self.config["prompts"]):
                self.idx = 0
            self.last_change = time.time()

        prompt = self.config["prompts"][self.idx]

        emotions = self.threshold(emotions, thr=0.7)
        colorization = self.emotions2colorization(emotions)

        return f"{prompt} | {colorization}"
