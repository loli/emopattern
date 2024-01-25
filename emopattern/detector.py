import threading
import asyncio
import base64
import os
import json

import cv2
import websockets


class EmotionDetector:
    def _init_(self):
        self.img = None
        self.hume_response = None
        self.img_updated = False
        self.lock = threading.Lock()
        self.start_emotion_detection()

    def update_image(self, img):
        with self.lock:
            self.img = img
            self.img_updated = True

    def get_hume_response(self):
        with self.lock:
            return self.hume_response

    def encode_frame(self, frame):
        ret, buffer = cv2.imencode(".jpg", frame)
        if not ret:
            raise ValueError("Could not encode frame")
        bytes_data = base64.b64encode(buffer)
        encoded_data = bytes_data.decode("utf-8")
        return encoded_data

    async def detect_emotions(self, frame):
        api_key = os.getenv("HUME_API_KEY")
        assert (
            api_key is not None
        ), "couldn't find HUME_API_KEY in environment variables"

        encoded_frame = self.encode_frame(frame)
        async with websockets.connect(
            "wss://api.hume.ai/v0/stream/models",
            extra_headers={"X-Hume-Api-Key": api_key},
        ) as websocket:
            message = {
                "models": {"face": {}},
                "data": encoded_frame,
                "raw_text": False,
            }
            await websocket.send(json.dumps(message))
            response = await websocket.recv()
            response_json = json.loads(response)
            return response_json

    def _detect_emotions_thread(self):
        while True:
            with self.lock:
                if self.img_updated and self.img is not None:
                    self.hume_response = asyncio.run(self.detect_emotions(self.img))

    def start_emotion_detection(self):
        threading.Thread(target=self._detect_emotions_thread, daemon=True).start()
