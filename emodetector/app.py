from flask import Flask, render_template, Response
from flask_socketio import SocketIO
import cv2
import base64
import asyncio
import websockets
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("X-Hume-Api-Key")

app = Flask(__name__)
socketio = SocketIO(app)


def encode_frame(frame):
    ret, buffer = cv2.imencode(".jpg", frame)
    if not ret:
        raise ValueError("Could not encode frame")
    bytes_data = base64.b64encode(buffer)
    encoded_data = bytes_data.decode("utf-8")
    return encoded_data


async def detect_emotions(frame):
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
        socketio.emit("new_data", {"result": response_json})


def gen_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode(".jpg", frame)
            frame_bytes = buffer.tobytes()
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
            )
            asyncio.run(send_frame_to_hume(frame))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    socketio.run(app, debug=True)
