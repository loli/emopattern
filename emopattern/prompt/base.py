from abc import ABCMeta, abstractmethod


class PromptGeneratorBase(metaclass=ABCMeta):
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
