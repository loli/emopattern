# emopattern

Closed-loop re-enforcement learning to trigger emotions.

The project consists of three apps: the _emotion detector_, which feeds from a webcam, detects the emotions of the viewer, and produced a prompt conditioned on them. The prompt is then send to the _stable diffusion model app_. That takes the prompt and produces a continuous stream of images, which it sends to the _viewer_ app. That can run on any other computer connected to a suitable monitor, TV or projector.

## Prepare

Create `.env` file in the main repo directory and add:

```
# the machine the stable diffusion model app runs on
export ZMQ_SERVER_IP="10.19.6.51"
export ZMQ_SERVER_PORT="5556"

# the machine the viewer runs on
export ZMQ_VIEWER_SERVER_IP="10.50.10.17"  # "10.50.10.254"
export ZMQ_VIEWER_SERVER_PORT="5557"

# the API keys required for the app
export OPENAI_API_KEY="XXX"
export HUME_API_KEY="XXX"
```

## Installation

`poetry install`

## Start virtual environment

`poetry shell`

## Run the emotion detector app

`poetry run python emopattern/app.py`

## Run the viewer app

`poetry run python emopattern/viewer.py`


## TODO

- Adapt server to read .env file, too
- Adapt server to use only server side of ZMQueque, viewer should request images
- Adapt detector to also allow prompt updates via keyboard
- Adapt detector to be robust against missing / errorneous openapi key
- Try to reduce viewer / detector dependencies (e.g. by extracting code from lunar-tools)