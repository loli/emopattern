from . import PromptGeneratorBase


class PromptGeneratorSimple(PromptGeneratorBase):
    def __init__(self):
        """Generates a prompt using the user input as scene description and the emotional reading as weighted adjectives.

        Example: A house on a hill, Joy+++, Fear+"""
        pass

    def get_prompt(self, emotions: dict[str, float], user_input: str | None = None):
        if user_input is None:
            user_input = self.DEFAULT_PROMPT

        emotions = self.topn(emotions, 3)
        colorization = self.emotions2colorization(emotions)

        return f"{user_input} | {colorization}"
