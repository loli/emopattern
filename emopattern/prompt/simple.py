from . import PromptGeneratorBase


class PromptGeneratorSimple(PromptGeneratorBase):
    def __init__(self):
        """Generates a prompt using the use input as scene description and the emotional reading as weighted adjectives."""
        pass

    def get_prompt(self, emotions: dict[str, float], user_input: str | None = None):
        colorization = ", ".join([f"{e}:{s * 10:.2f}" for e, s in emotions.items()])

        # colorization = " and ".join([e for e, _ in emotions.items()])

        emoplusses = [f"{e}" + "+" * int(s * 10) for e, s in emotions.items()]
        colorization = ", ".join(emoplusses)

        if user_input is None:
            user_input = self.DEFAULT_PROMPT

        return f"{colorization}, {user_input}"
