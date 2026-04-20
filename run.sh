#!/usr/bin/env bash

cd "$(dirname "$0")"

uv venv venv --python 3.11
source venv/bin/activate
uv pip install -e ".[cli,dev]"
export API_SERVER_ENABLED=true 
export API_SERVER_HOST=127.0.0.1 
export API_SERVER_PORT=8642 
uv run hermes gateway run
