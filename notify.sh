#!/usr/bin/env bash

# shellcheck disable=SC1091
. ./set_apikeys.sh || exit 1;
. ./activate_env.sh || exit 1;

chinfo="chinfo.csv"
mslog_root_path="milestone_log"

. ./parse_options.sh || exit 1;

python -m subscbot.bin.notify_milestone \
    --chinfo "${chinfo}" \
    --mslog_root_path "${mslog_root_path}"
