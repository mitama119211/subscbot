#!/usr/bin/env bash

# shellcheck disable=SC1091
. ./activate_env.sh || exit 1;

conf="conf/config.yaml"
verbose=1

. ./parse_options.sh || exit 1;

python -m subscbot.bin.notify_milestone \
    --conf "${conf}" \
    --verbose "${verbose}"
