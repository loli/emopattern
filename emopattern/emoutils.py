# Emotion manipulation utilities

import json
import logging

logger = logging.getLogger(__name__)

EMOTIONS_THRESHOLD = (
    0.3  # all emotions with a likelihood under this value are filtered out
)
EMOTIONS_VALID = [
    "Calmness",
    "Joy",
    "Amusement",
    "Anger",
    "Confusion",
    "Disgust",
    "Sadness",
    "Horror",
    "Surprise",
]  # only these emotions are kept, others are dropped


def emotions_get_sample():
    # !TODO: Change to use importlib.resources
    return {}
    # with open("resources/emoexample.json") as f:
    #    return json.load(f)


def emotions_process_and_filter(humeai_response: dict) -> dict | None:
    "Pre-process and filter emotions."
    if "warning" in humeai_response["face"]:
        logger.debug(
            f"hume.ai failed to detect a face: {humeai_response['face']['warning']}"
        )
        return None
    if len(humeai_response["face"]["predictions"]) > 0:
        logger.debug("hume.ai detect more than one face. Dropping all but first.")

    prediction = humeai_response["face"]["predictions"][0]

    if prediction["prob"] < 0.5:
        logger.warn("Predicted face has probability < 0.5. Skipping.")
        return None

    emotions = prediction["emotions"]

    emotions = {e["name"]: e["score"] for e in emotions if e["name"] in EMOTIONS_VALID}

    emotions = {k: v for k, v in emotions.items() if v >= EMOTIONS_THRESHOLD}

    return emotions


def emotions_smooth(emotions, emotions_history=[]):
    "Smooth emotion value based on emotion history to avoid sudden jumps."
    return emotions
