from . import PromptGeneratorBase


class PromptGeneratorSimple(PromptGeneratorBase):
    BASE_PROMPT = "highly cinematic photo showing a scene from a dream, photography, film still, shot on kodak"

    def get_prompt(self, emotions: dict[str, float], user_input: str | None = None):
        colorization = ", ".join([f"{e}: {s * 2:.2f}" for e, s in emotions.items()])

        return f"{self.BASE_PROMPT}, {colorization}"
