#!/usr/bin/bash

# shellcheck disable=SC1091
. ./set_apikeys.sh
. ./activate_env.sh

if [ -n "${API_KEY}" ] && [ -n "${API_KEY_SECRET}" ] &&[ -n "${DEVELOPER_KEY}" ]; then
    python -m subscbot.bin.authenticate
else
    echo "Please set API_KEY, API_KEY_SECRET and DEVELOPER_KEY in \"set_apikeys.sh\"."
    exit 1
fi
