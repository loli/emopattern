# Emotion manipulation utilities

import logging

logger = logging.getLogger(__name__)


def preprocess(humeai_response: dict) -> dict[str, float] | None:
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

    return {e["name"]: e["score"] for e in prediction["emotions"]}
