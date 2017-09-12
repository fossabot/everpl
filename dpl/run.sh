#!/bin/bash

SCRIPT_PATH="$(readlink -f "$0")"
DPL_PATH="$(dirname "$SCRIPT_PATH")"
DPL_PARENT_PATH="$(dirname "$DPL_PATH")"

export PYTHONPATH="$DPL_PARENT_PATH:$PYTHONPATH"

python3 "$DPL_PATH/run.py" "$@"
