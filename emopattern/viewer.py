#!/usr/bin/env python3
# viewer app, simply reciving images from the stable diffusion app

import os
import logging
import argparse
import time
import lunar_tools as lt
from dotenv import load_dotenv

CAMERA_RES_X = 1024
CAMERA_RES_Y = 1024

load_dotenv()
logger = logging.getLogger(__name__)
zmq_client = lt.ZMQPairEndpoint(
    is_server=True,
    ip=os.getenv("ZMQ_VIEWER_SERVER_IP"),
    port=os.getenv("ZMQ_VIEWER_SERVER_PORT"),
)


def main():
    args = get_parser().parse_args()

    # config
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    renderer = lt.Renderer(height=CAMERA_RES_Y, width=CAMERA_RES_X, backend="opencv")

    logger.info("Starting...")

    while True:
        image = zmq_client.get_img()
        if image is not None:
            renderer.render(image)


def get_parser():
    parser = argparse.ArgumentParser(
        prog="viewer",
        description="Viewer, aka renderer for the stable diffusion app's images",
    )
    parser.add_argument("-d", "--debug", help="Debug messages.", action="store_true")
    return parser


if __name__ == "__main__":
    main()
