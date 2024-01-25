import os
import time
import logging
import asyncio
import argparse

import lunar_tools as lt
from dotenv import load_dotenv

from emopattern import emoutils, humeutils
from emopattern.prompt import PromptGeneratorSimple
from emopattern.detector import EmotionDetector

load_dotenv()
logger = logging.getLogger(__name__)

CAMERA_RES_Y = 480
CAMERA_RES_X = 640


def main():
    args = get_parser().parse_args()

    # config
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    # inits
    keyboard_input = lt.KeyboardInput()
    cam = lt.WebCam(shape_hw=(CAMERA_RES_Y, CAMERA_RES_X))
    renderer = lt.Renderer(height=CAMERA_RES_Y, width=CAMERA_RES_X, backend="opencv")
    speech_detector = lt.Speech2Text()
    zmq_client = lt.ZMQPairEndpoint(
        is_server=False,
        ip=os.getenv("ZMQ_SERVER_IP"),
        port=os.getenv("ZMQ_SERVER_PORT"),
    )
    promptgen = PromptGeneratorSimple()
    recording = None
    detector = EmotionDetector()

    logger.info("Starting...")
    logger.debug("DEBUG")

    while True:
        time.sleep(0.1)
        # capture new voice recording
        recording_start = keyboard_input.get("r", button_mode="pressed_once")
        if recording_start:
            logger.info("Recording started...")
            speech_detector.start_recording()

        recording_stop = keyboard_input.get("r", button_mode="released_once")
        if recording_stop:
            logger.info("Recording finished")
            recording = speech_detector.stop_recording()
            logger.debug(f"Recorded text: {recording}")

        # capture next frame & process
        img = cam.get_img()

        logger.info("Detecting emotions...")
        # hume_response = asyncio.run(humeutils.detect_emotions(img))
        detector.update_image(img)
        hume_response = detector.get_hume_response()
        print(hume_response)
        logger.info("Processing emotions...")
        emotions = emoutils.emotions_process_and_filter(hume_response)
        logger.info(f"Found: {emotions}")

        if emotions is None:
            continue

        # construct prompt
        prompt = promptgen.get_prompt(emotions, recording)
        logger.info(f"Colored prompt: {prompt}")

        # send result to image generator
        logger.info("Message prompt..")
        zmq_client.send_json({"prompt": prompt})
        renderer.render(img)


def get_parser():
    parser = argparse.ArgumentParser(
        prog="emopattern",
        description="Emotion capture through the webcam and scene change through input",
    )
    parser.add_argument("-d", "--debug", help="Debug messages.", action="store_true")
    return parser


if __name__ == "__main__":
    main()
