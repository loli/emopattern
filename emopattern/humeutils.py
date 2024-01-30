# hume.ai based emotion detection utilities
import os
import json
import base64

import cv2
import websockets


def encode_frame(frame):
    ret, buffer = cv2.imencode(".jpg", frame)
    if not ret:
        raise ValueError("Could not encode frame")
    bytes_data = base64.b64encode(buffer)
    encoded_data = bytes_data.decode("utf-8")
    return encoded_data


async def detect_emotions(frame):
    api_key = os.getenv("HUME_API_KEY")
    assert api_key is not None, "couldn't find HUME_API_KEY in environment variables"

    encoded_frame = encode_frame(frame)
    async with websockets.connect(
        "wss://api.hume.ai/v0/stream/models", extra_headers={"X-Hume-Api-Key": api_key}
    ) as websocket:
        message = {
            "models": {
                # Specify the models you want to use, e.g., "face": {}
                "face": {}
            },
            "data": encoded_frame,
            "raw_text": False,  # Set to True if sending text, False for images/audio
        }
        await websocket.send(json.dumps(message))
        response = await websocket.recv()
        response_json = json.loads(response)
        return response_json
