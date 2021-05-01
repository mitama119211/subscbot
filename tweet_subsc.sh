#!/usr/bin/env bash

# shellcheck disable=SC1091
. ./activate_env.sh || exit 1;

conf="conf/config.yaml"
tweet_type=""
verbose=1

. ./parse_options.sh || exit 1;

python -m subscbot.bin.tweet_subscribers \
    --conf "${conf}" \
    --tweet_type "${tweet_type}" \
    --verbose "${verbose}"
