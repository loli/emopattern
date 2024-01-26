import importlib.resources

import yaml

from . import PromptGeneratorBase


class PromptGeneratorEmostrings(PromptGeneratorBase):
    def __init__(self, promptfile: str):
        """Creates prompt based on randomly selected scenes and an LLM response utilizing the highest scoring emotion in the reading.

        Args:
            promptfile: YAML file containint the prompts strings for the different emotions.
                Expected format is `emotion: str`, aka `Joy: "vibrant colors, joyful scenes, smiling faces"`

        Example: A house on a hill. Generate an image capturing a moment of genuine surprise, with dynamic elements and expressions that elicit a sense of astonishment and wonder.
        """
        with importlib.resources.files("emopattern.resources").joinpath(
            promptfile
        ).open("rb") as f:
            self.config = yaml.safe_load(f)

    def get_prompt(self, emotions: dict[str, float], user_input: str | None = None):
        prompt = self.DEFAULT_PROMPT if user_input is None else user_input
        prompt += "."

        # filter down to know emotions
        emotions = {e: s for e, s in emotions.items() if e in self.config}

        if len(emotions) < 0:
            return prompt
        else:
            primary_emotion = max(
                emotions, key=emotions.get
            )  # keep only most likely emotion
            return f"{prompt} | {self.config[primary_emotion]}"
