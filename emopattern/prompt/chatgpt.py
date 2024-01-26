import logging
import importlib.resources

import yaml
import lunar_tools as lt

from . import PromptGeneratorBase

logger = logging.getLogger(__name__)


class PromptGeneratorChatGPT(PromptGeneratorBase):
    def __init__(self):
        """Creates a prompt using ChatGPT to incorporate the emotions."""
        self.chatgpt4 = lt.GPT4()
        with importlib.resources.files("emopattern.resources").joinpath(
            "mirroring_woimage.yaml"
        ).open("rb") as f:
            self.config = yaml.safe_load(f)

    def get_prompt(self, emotions: dict[str, float], user_input: str | None = None):
        if user_input is None:
            topic = "The bible."
        else:
            topic = user_input

        emotions = self.topn(emotions, 1)
        emotions = ", ".join(emotions.keys())

        llm_prompt_scene = f"""
        Respond with a short description of a scene from the following topic: {topic}.
        
        Take care to pick a scene that conveys the following emotions best: {emotions}
        """
        scene = self.chatgpt4.generate(llm_prompt_scene)

        llm_prompt_prompt = f"""
        Respond with an input prompt for a stable diffusion model.
        The prompt should be very short, best descibed in one image.
        The prompt should cause the stable diffusion model to generate an image of the following scene: {scene}
        """
        prompt = self.chatgpt4.generate(llm_prompt_prompt)

        return f"{prompt} | very emotional, emotions clearly visible, emotional colours | {emotions}+++++"
