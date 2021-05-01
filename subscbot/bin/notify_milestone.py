"""Check and notify milestones."""
import argparse
import datetime
import os
import sys

from logging import basicConfig
from logging import getLogger

import pandas as pd
import yaml

from apiclient.discovery import build
from requests_oauthlib import OAuth1Session

from subscbot.twitter_api import update
from subscbot.youtube_api import get_subscribers


def check_notified(chid_subsc_list, chinfo, MILESTONE_L=10000):
    """Notify when one has less than 100 people left to reach MILESTONE_L."""
    """NOTE: Is this function needed?"""
    notifiedlog_filename = "notified.log"

    notified_list = []
    for chid, subscribers in chid_subsc_list:
        notifiedlog_path = chinfo[chinfo["chid"] == chid]["mslog_path"].values[0]
        notifiedlog_file = os.path.join(notifiedlog_path, notifiedlog_filename)
        next_milestone = (subscribers//MILESTONE_L + 1) * MILESTONE_L
        remain = 100 if (next_milestone - subscribers) <= 100 else -1

        if not os.path.exists(notifiedlog_file):
            with open(notifiedlog_file, "w") as f:
                if remain == -1:
                    f.write(str(subscribers//MILESTONE_L * MILESTONE_L))
                else:
                    f.write(str(next_milestone-remain))
        else:
            with open(notifiedlog_file, "r") as f:
                prev_notified = int(f.read())

            if remain != -1 and prev_notified < (next_milestone-remain):
                notified_list.append((chid, next_milestone, next_milestone-subscribers))
                with open(notifiedlog_file, "w") as f:
                    f.write(str(next_milestone-remain))

    return notified_list


def check_milestone(chid_subsc_list, chinfo, MILESTONE_S=1000):
    """Check whether the number of subscribers exceeds the milestone number."""
    mslog_filename = "milestone.log"

    milestone_list = []
    for chid, subscribers in chid_subsc_list:
        mslog_path = chinfo[chinfo["chid"] == chid]["mslog_path"].values[0]
        mslog_file = os.path.join(mslog_path, mslog_filename)
        reached_milestone = subscribers//MILESTONE_S * MILESTONE_S

        if not os.path.exists(mslog_file):
            with open(mslog_file, "w") as f:
                f.write(str(reached_milestone))
        else:
            with open(mslog_file, "r") as f:
                prev_milestone = int(f.read())

            if prev_milestone < reached_milestone:
                milestone_list.append((chid, reached_milestone, subscribers))
                with open(mslog_file, "w") as f:
                    f.write(str(reached_milestone))

    return milestone_list


def get_arguments():
    """Get arguments."""
    parser = argparse.ArgumentParser(description="CHeck and notify milestones.")
    parser.add_argument("--conf", type=str, default="conf/config.yaml",
                        help="Path to a config file with API keys.")
    parser.add_argument("--verbose", type=int, default=1,
                        help="Logging level.")

    return parser.parse_args()


def main():
    """Tweet notification of a milestone timing."""
    # get arguments
    args = get_arguments()

    # set logger
    if args.verbose > 1:
        from logging import DEBUG
        basicConfig(
            level=DEBUG, stream=sys.stdout,
            format="%(asctime)s (%(module)s:%(lineno)d) %(levelname)s: %(message)s")
    elif args.verbose == 1:
        from logging import INFO
        basicConfig(
            level=INFO, stream=sys.stdout,
            format="%(asctime)s (%(module)s:%(lineno)d) %(levelname)s: %(message)s")
    else:
        from logging import WARN
        basicConfig(
            level=WARN, stream=sys.stdout,
            format="%(asctime)s (%(module)s:%(lineno)d) %(levelname)s: %(message)s")
    logger = getLogger(__name__)

    # load config
    with open(args.conf, mode="r") as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)

    # get API keys
    api_keys = config.get("api_keys", "")
    try:
        DEVELOPER_KEY = api_keys["DEVELOPER_KEY"]
        API_KEY = api_keys["API_KEY"]
        API_KEY_SECRET = api_keys["API_KEY_SECRET"]
        ACCESS_TOKEN = api_keys["ACCESS_TOKEN"]
        ACCESS_TOKEN_SECRET = api_keys["ACCESS_TOKEN_SECRET"]
    except KeyError:
        logger.error("API keys must be specified.")
        sys.exit(1)
    if not all(api_keys.values()):
        logger.error("API keys must be specified.")
        sys.exit(1)

    # load channel info
    # chinfo: (chid, name, dirname)
    chinfo = pd.read_csv(config["chinfo"])

    # check log dirctory existance
    mslog_root_path = config.get("mslog_root_path", "milestone_log")
    if not os.path.exists(mslog_root_path):
        os.makedirs(mslog_root_path)
        logger.info(f"Create {mslog_root_path}")
    mslog_path_list = [os.path.join(mslog_root_path, dirname) for dirname in chinfo["dirname"]]
    chinfo["mslog_path"] = mslog_path_list
    for mslog_path in mslog_path_list:
        if not os.path.exists(mslog_path):
            os.mkdir(mslog_path)
            logger.info(f"Create {mslog_path}")

    # get current time
    datetime_now = datetime.datetime.now()
    # set timestamp (YYYY-MM-DD_hh:mm:ss)
    timestamp = datetime_now.strftime("%Y-%m-%d_%H:%M:%S")

    # launch a session
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY, cache_discovery=False)
    twitter = OAuth1Session(API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # get the number of subscribers
    chids = ",".join(chinfo["chid"])
    chid_subsc_list = get_subscribers(youtube=youtube, chids=chids)

    notified_list = check_notified(chid_subsc_list, chinfo=chinfo, MILESTONE_L=config.get("MILESTONE_L", 10000))
    milestone_list = check_milestone(chid_subsc_list, chinfo=chinfo, MILESTONE_S=config.get("MILESTONE_S", 1000))

    status_list = []
    for chid, next_criterion, diff in notified_list:
        name = chinfo[chinfo["chid"] == chid]["name"].values[0]
        status = f"{timestamp}\n"
        status += f"#{name} さんのチャンネル登録者数{next_criterion:,d}人まで残り{diff:,d}人です。"
        status_list.append(status)
    for chid, reached_milestone, subscribers in milestone_list:
        name = chinfo[chinfo["chid"] == chid]["name"].values[0]
        status = f"{timestamp}\n"
        status += f"#{name} さんのチャンネル登録者数が{reached_milestone:,d}人を達成しました！\n"
        status += f"現在: {subscribers:,d}人"
        status_list.append(status)
    for status in status_list:
        update(twitter=twitter, status=status)
        logger.debug(status)


if __name__ == "__main__":
    main()
