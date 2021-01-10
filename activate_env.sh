#!/usr/bin/env bash

if [ -e ./env/venv/bin/activate ]; then
    # shellcheck disable=SC1091
    . ./env/venv/bin/activate
else
    echo "Please run \"make\" in ./env before."
    exit 1
fi