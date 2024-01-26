# emopattern

Closed-loop re-enforcement learning to trigger emotions

## Prepare

Create `.env` file in the main repo directory and add:

```
export ZMQ_SERVER_IP = "10.50.10.15"
export ZMQ_SERVER_PORT = "5556"

export OPEN_AI_KEY="XXX"
export HUME_API_KEY="XXX"
```

## Installation

`poetry install`

## Start virtual environment

`poetry shell`

## Run the emotion detector app

`poetry run python emopattern/app.py`
