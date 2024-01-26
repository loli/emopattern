import os
import time
import logging
import asyncio
import argparse

import lunar_tools as lt
from dotenv import load_dotenv

from concurrent.futures import ThreadPoolExecutor

from emopattern import emoutils, humeutils
from emopattern.prompt import (
    PromptGeneratorSimple,
    PromptGeneratorEmostrings,
    PromptGeneratorMirror,
    PromptGeneratorShuffle,
    PromptGeneratorChatGPT,
)


CAMERA_RES_Y = 480
CAMERA_RES_X = 640


load_dotenv()
logger = logging.getLogger(__name__)
zmq_client = lt.ZMQPairEndpoint(
    is_server=False,
    ip=os.getenv("ZMQ_SERVER_IP"),
    port=os.getenv("ZMQ_SERVER_PORT"),
)

# prompt generation schema
# promptgen = PromptGeneratorSimple()
# promptgen = PromptGeneratorEmostrings("emoprompts.yaml")
# promptgen = PromptGeneratorEmostrings("emostrings_short.yaml")
# promptgen = PromptGeneratorMirror()
# promptgen = PromptGeneratorShuffle("shuffle2.yaml")

# promptgen = PromptGeneratorSimple()
promptgen = PromptGeneratorEmostrings("emostrings_short.yaml")
# promptgen = PromptGeneratorShuffle("shuffle3.yaml", seconds=90)
# promptgen = PromptGeneratorChatGPT()


def main():
    args = get_parser().parse_args()

    # config
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    # inits
    keyboard_input = lt.KeyboardInput()
    cam = lt.WebCam(shape_hw=(CAMERA_RES_Y, CAMERA_RES_X), cam_id=args.camera)
    renderer = lt.Renderer(height=CAMERA_RES_Y, width=CAMERA_RES_X, backend="opencv")
    speech_detector = lt.Speech2Text()

    executor = ThreadPoolExecutor(max_workers=1)
    recording = None

    logger.info("Starting...")

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

        if executor._work_queue.qsize() == 0:
            logger.info("Detecting emotions...")
            hume_future = executor.submit(
                lambda img: asyncio.run(humeutils.detect_emotions(img)), img
            )
            hume_future.add_done_callback(
                lambda future: process_emotion_and_send(future, recording)
            )

        renderer.render(img)


def process_emotion_and_send(future, recording) -> None:
    logger.info("Processing emotions...")
    emotions = emoutils.preprocess(future.result())
    logger.info(f"Found: {emotions}")

    if emotions is None:
        return

    # construct prompt
    prompt = promptgen.get_prompt(emotions, recording)
    logger.info(f"Colored prompt: {prompt}")

    # send result to image generator
    logger.info("Message prompt..")
    zmq_client.send_json({"prompt": prompt})


def get_parser():
    parser = argparse.ArgumentParser(
        prog="emopattern",
        description="Emotion capture through the webcam and scene change through input",
    )
    parser.add_argument(
        "--camera", help="Camera to use, from 0 to X.", type=int, default=0
    )
    parser.add_argument("-d", "--debug", help="Debug messages.", action="store_true")
    return parser


if __name__ == "__main__":
    main()
