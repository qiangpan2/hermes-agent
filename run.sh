#!/usr/bin/env bash

cd "$(dirname "$0")"

uv venv venv --python 3.11
source venv/bin/activate
uv pip install -e ".[cli,dev]"
export HERMES_HOME="$PWD/.hermes"
mkdir -p "$HERMES_HOME"
[ -f "$HERMES_HOME/.env" ] || cp .env.example "$HERMES_HOME/.env"
uv run hermes gateway run
