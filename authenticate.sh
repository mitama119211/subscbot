#!/usr/bin/env bash

# shellcheck disable=SC1091
. ./set_apikeys.sh || exit 1;
. ./activate_env.sh || exit 1;

oauth_callback=""

. ./parse_options.sh || exit 1;

if [ -z "${oauth_callback}" ]; then
    echo "Usage: ./authenticate.sh --oauth_callback OAUTH_CALLBACK"
    echo "Please specify --oauth_callback"
    exit 1
fi

if [ -n "${API_KEY}" ] && [ -n "${API_KEY_SECRET}" ] &&[ -n "${DEVELOPER_KEY}" ]; then
    python -m subscbot.bin.authenticate \
        --oauth_callback "${oauth_callback}"
else
    echo "Please set API_KEY, API_KEY_SECRET and DEVELOPER_KEY in \"set_apikeys.sh\"."
    exit 1
fi
