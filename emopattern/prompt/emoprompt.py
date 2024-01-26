import importlib.resources

import yaml

from . import PromptGeneratorBase


class PromptGeneratorEmoprompt(PromptGeneratorBase):
    def __init__(self):
        """Creates prompt based on randomly selected scenes and an LLM response utilizing the emotion reading.

        Example: A house on a hill. Generate an image capturing a moment of genuine surprise, with dynamic elements and expressions that elicit a sense of astonishment and wonder.
        """
        with importlib.resources.files("emopattern.resources").joinpath(
            "emoprompts.yaml"
        ).open("rb") as f:
            # with open("emopattern/resources/emoprompts.yaml", "r") as f:
            self.config = yaml.safe_load(f)

    def get_prompt(self, emotions: dict[str, float], user_input: str | None = None):
        prompt = self.DEFAULT_PROMPT if user_input is None else user_input
        prompt += "."

        for e in emotions.keys():
            if e in self.config:
                prompt += " " + self.config[e]

        return prompt
