import logging
import importlib.resources

import yaml
import lunar_tools as lt

from . import PromptGeneratorBase

logger = logging.getLogger(__name__)


class PromptGeneratorMirror(PromptGeneratorBase):
    def __init__(self):
        """Creates a prompt using ChatGPT to incorporate the emotions into a selected scene.

        Example: !TBD
        """
        self.chatgpt4 = lt.GPT4()
        with importlib.resources.files("emopattern.resources").joinpath(
            "mirroring_woimage.yaml"
        ).open("rb") as f:
            self.config = yaml.safe_load(f)

    def get_prompt(self, emotions: dict[str, float], user_input: str | None = None):
        scene = self.config["scenes"][0]

        emotion_string = self.__parse_emotions(emotions)
        logger.info(emotion_string)

        llm_prompt = self.config["llm_prompt"]
        llm_prompt.format(scene=scene, emotions=emotion_string)

        llm_scene = self.chatgpt4.generate(llm_prompt)

        prompt = self.config["sd_prompt"]
        prompt = prompt.format(llm_scene=llm_scene)

        return prompt

    def __parse_emotions(self, emotions):
        emotion_strings = []
        for e, s in emotions.items():
            if s > 0.5:
                if s > 0.8:
                    emotion_strings.append(f"high {e}")
                # else:
                #    emotion_strings.append(f"low {e}")

        return ", ".join(emotion_strings)
