#!/usr/bin/env bash

# shellcheck disable=SC1091
. ./set_apikeys.sh || exit 1;
. ./activate_env.sh || exit 1;

chinfo="chinfo.csv"
log_root_path="subscribers_log"
tweet_type="image"

. ./parse_options.sh || exit 1;

python -m subscbot.bin.tweet_subscribers \
    --chinfo "${chinfo}" \
    --log_root_path "${log_root_path}" \
    --tweet_type "${tweet_type}"
