#!/usr/bin/env bash

# shellcheck disable=SC1091
. ./activate_env.sh || exit 1;

conf="conf/config.yaml"
oauth_callback=""
verbose=1

. ./parse_options.sh || exit 1;

if [ -n "${oauth_callback}" ]; then
    python -m subscbot.bin.authenticate \
        --conf "${conf}" \
        --oauth_callback "${oauth_callback}" \
        --verbose "${verbose}"
else
    echo "Usage: ./authenticate.sh --oauth_callback <oauth_callback>"
    echo "Please specify --oauth_callback"
    exit 1
fi
