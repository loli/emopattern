from abc import ABCMeta, abstractmethod


class PromptGeneratorBase(metaclass=ABCMeta):
    DEFAULT_PROMPT = "highly cinematic photo showing a scene from a dream, photography, film still, shot on kodak"
    # DEFAULT_PROMPT = "Generate a surreal dreamscape landscape that transcends reality, featuring fantastical elements, vibrant colors, and ethereal lighting. Convey a sense of wonder, whimsy, and imaginative exploration, as if the viewer has stepped into a dream world filled with magical landscapes and otherworldly beauty."

    @abstractmethod
    def get_prompt(
        self, emotions: dict[str, float], user_input: str | None = None
    ) -> str:
        """Return the prompt generated to the implemented strategy.

        Args:
            emotions: detected emotions in the format {emotion: score} where score in [0,1]
            user_input: user input that can be used to steer the prompt generation

        Returns:
            generated prompt, ready to be consumed by stable diffusion, prompt weighting supported

        """
        pass
