# emopattern-server
Runs [Stable Diffusion SDXL Turbo](https://stability.ai/news/stability-ai-sdxl-turbo) to generate image in real time based on a prompt send via a ZMQ Queque.

Ensures smooth transitions between the prompt images.

Sends back the images via ZMQ Queque to a rendering app.

## Installation

`poetry install`

## Start virtual environment

`poetry shell`

## Run the emopattern model server app

`poetry run python turbo_renderer.py`