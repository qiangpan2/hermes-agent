#!/usr/bin/env bash

cd "$(dirname "$0")"

uv venv venv --python 3.11
source venv/bin/activate
uv pip install -e ".[cli,dev]"
export HERMES_HOME="$PWD/.hermes"
mkdir -p "$HERMES_HOME"
[ -f "$HERMES_HOME/.env" ] || cp .env.example "$HERMES_HOME/.env"
mkdir -p "$HERMES_HOME/plugins"
[ -e "$HERMES_HOME/plugins/rapid" ] || ln -s "$PWD/RAPID-Plugins" "$HERMES_HOME/plugins/rapid"
uv run hermes gateway run
