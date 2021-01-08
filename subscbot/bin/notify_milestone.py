import argparse
import datetime
import os

import pandas as pd

from subscbot.twitter_api import statuses_update
from subscbot.youtube_api import get_subscribers

MILESTONE_L = 10000
MILESTONE_S = 1000


def check_notified(chid_subsc_list, chinfo):
    """Notify when one has less than 100 people left to reach MILESTONE_L."""
    """NOTE: Is this function needed?"""
    notifiedlog_filename = "notified.log"

    notify_list = []
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
                notify_list.append((chid, next_milestone, next_milestone-subscribers))
                with open(notifiedlog_file, "w") as f:
                    f.write(str(next_milestone-remain))

    return notify_list


def check_milestone(chid_subsc_list, chinfo):
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
    parser = argparse.ArgumentParser(description="Tweet the number of subscribers with text or an image.")
    parser.add_argument("--chinfo", type=str, default="chinfo.csv")
    parser.add_argument("--mslog_root_path", type=str, default="milestone_log")

    return parser.parse_args()


def main():
    """Tweet notification of a milestone timing."""
    # get arguments
    args = get_arguments()

    # load channel info
    # chinfo: (chid, name, dirname)
    chinfo = pd.read_csv("chinfo.csv")

    # check log dirctory existance
    mslog_root_path = args.mslog_root_path
    if not os.path.exists(mslog_root_path):
        os.makedirs(mslog_root_path)
    mslog_path_list = [os.path.join(mslog_root_path, dirname) for dirname in chinfo["dirname"]]
    chinfo["mslog_path"] = mslog_path_list
    for mslog_path in mslog_path_list:
        if not os.path.exists(mslog_path):
            os.mkdir(mslog_path)

    # get current time
    datetime_now = datetime.datetime.now()
    # set timestamp (YYYY-MM-DD_hh:mm:ss)
    timestamp = datetime_now.strftime("%Y-%m-%d_%H:%M:%S")

    # get the number of subscribers
    chids = ",".join(chinfo["chid"])
    chid_subsc_list = get_subscribers(chids)

    notify_list = check_notified(chid_subsc_list, chinfo=chinfo)
    milestone_list = check_milestone(chid_subsc_list, chinfo=chinfo)

    status_list = []
    for chid, next_criterion, diff in notify_list:
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
        statuses_update(status)


if __name__ == "__main__":
    main()