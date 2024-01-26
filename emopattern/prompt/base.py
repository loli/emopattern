import logging
from abc import ABCMeta, abstractmethod

logger = logging.getLogger(__name__)


class PromptGeneratorBase(metaclass=ABCMeta):
    DEFAULT_PROMPT = "Mysterious creature coming out of the night sky"  # defaut prompt use when required
    DEFAULT_PROMPT = (
        "A very emotional moment. The subjectt's emotions are clearly readable."
    )
    EMOTIONS_THRESHOLD = (
        0.3  # default minimal likelihood an emotion has to reach to be considered
    )
    EMOTIONS_PRIMARY = [
        "Calmness",
        "Joy",
        "Amusement",
        "Anger",
        "Confusion",
        "Disgust",
        "Sadness",
        "Horror",
        "Surprise",
    ]  # default list of primary emotions, can be used to filter

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

    def filter_to_primary(
        self,
        emotions: dict[str, float],
        valid: list[str] | None = None,
    ) -> dict[str, float]:
        """Filter the emotions, returning only the once considered primary."""
        if valid is None:
            valid = self.EMOTIONS_PRIMARY
        return {e: s for e, s in emotions.items() if e in valid}

    def threshold(
        self,
        emotions: dict[str, float],
        thr: float | None = None,
    ) -> dict[str, float]:
        """Filter emotions whose likelihood does not meet the threshold criteria."""
        if thr is None:
            thr = self.EMOTIONS_THRESHOLD
        return {e: s for e, s in emotions.items() if s >= thr}

    def toponly(self, emotions):
        "Returns a dict with only the highest ranking emotion."
        return self.topn(emotions, 1)

    def topn(self, emotions, n):
        "Returns dict wiht the top-N emotions."
        emotions = sorted(emotions.items(), key=lambda x: x[1])[::-1][:n]
        return {x[0]: x[1] for x in emotions}

    def emotions2colorization(self, emotions):
        "Turn emotions dict into weighted emotuion adjectives joined into a string"
        emoplusses = [f"{e}" + "+" * int(s * 10) for e, s in emotions.items()]
        colorization = ", ".join(emoplusses)
        return colorization
