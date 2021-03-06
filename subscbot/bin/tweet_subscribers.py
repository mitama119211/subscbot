"""Tweet the number of subscribers with text or an image."""
import argparse
import datetime
import os
import sys

from logging import basicConfig
from logging import getLogger

import japanize_matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import yaml

from apiclient.discovery import build
from requests_oauthlib import OAuth1Session

from subscbot.twitter_api import update
from subscbot.twitter_api import upload
from subscbot.youtube_api import get_subscribers


def output_log(datetime_now, chid_subsc_list, chinfo):
    """Output logs of the number of subscribers."""
    # set timestamp (YYYY-MM-DD_hh:mm:ss)
    timestamp = datetime_now.strftime("%Y-%m-%d_%H:%M:%S")

    # set log file name (YYYYMM.log)
    log_filename = f"{datetime_now.strftime('%Y%m')}.log"

    for chid, subscribers in chid_subsc_list:
        log = f"{timestamp} {subscribers:7d}"

        # NOTE: not sophisticated
        log_path = chinfo[chinfo["chid"] == chid]["log_path"].values[0]
        log_file = os.path.join(log_path, log_filename)
        if os.path.exists(log_file):
            with open(log_file, "a") as f:
                f.write(f"\n{log}")
        else:
            with open(log_file, "w") as f:
                f.write(log)


def check_prev_subsc(chid_subsc_list, chinfo, prevlog_filename="prev_subscribers.log"):
    """Check the previous log."""
    prev_subsc_dict = dict()
    for chid, subscribers in chid_subsc_list:
        # NOTE: not sophisticated
        log_path = chinfo[chinfo["chid"] == chid]["log_path"].values[0]
        prevlog_path = os.path.join(log_path, prevlog_filename)

        prev_subscribers = None
        if os.path.exists(prevlog_path):
            with open(prevlog_path, "r") as f:
                prev_subscribers = int(f.read())
        with open(prevlog_path, "w") as f:
            f.write(str(subscribers))
        prev_subsc_dict[chid] = prev_subscribers

    return prev_subsc_dict


def form_name(name, nmax=8):
    """Format the length of the name."""
    return "＿"*(nmax-len(name)) + name


def get_arguments():
    """Get arguments."""
    parser = argparse.ArgumentParser(description="Tweet the number of subscribers with text or an image.")
    parser.add_argument("--conf", type=str, default="conf/config.yaml",
                        help="Path to a config file with API keys.")
    parser.add_argument("--tweet_type", type=str, default="",
                        help="How to tweet.")
    parser.add_argument("--verbose", type=int, default=1,
                        help="Logging level.")

    return parser.parse_args()


def main():
    """Tweet the number of subscribers with text or an image."""
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
    log_root_path = config.get("log_root_path", "subscribers_log")
    if not os.path.exists(log_root_path):
        os.makedirs(log_root_path)
        logger.info(f"Create {log_root_path}")
    log_path_list = [os.path.join(log_root_path, dirname) for dirname in chinfo["dirname"]]
    chinfo["log_path"] = log_path_list
    for log_path in log_path_list:
        if not os.path.exists(log_path):
            os.mkdir(log_path)
            logger.info(f"Create {log_path}")

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

    # output logs of the number of subscribers
    output_log(datetime_now, chid_subsc_list, chinfo=chinfo)

    # tweet the number of subscribers
    tweet_type = config.get("tweet_type", "image") if not args.tweet_type else args.tweet_type
    prev_subsc_dict = check_prev_subsc(chid_subsc_list, chinfo=chinfo)
    # FIXME: "text" doesn't work
    #        status_list should be divided considering the word limit.
    if tweet_type == "text":
        status_list = []
        nmax = max([len(name) for name in chinfo["name"]])
        for chid, subsc in chid_subsc_list:
            prev_subsc = prev_subsc_dict.get(chid)
            # NOTE: not sophisticated
            name = chinfo[chinfo["chid"] == chid]["name"].values[0]
            if prev_subsc is not None:
                diff = subsc - prev_subsc
                if diff != 0:
                    status_list.append(
                        f"{form_name(name, nmax=nmax):s}: {subsc:_=8,d} ({subsc-prev_subsc:+})"
                    )
                else:
                    status_list.append(
                        f"{form_name(name, nmax=nmax):s}: {subsc:_=8,d} (0)"
                    )
            else:
                status_list.append(
                    f"{form_name(name, nmax=nmax):s}: {subsc:_=8,d}"
                )
        exit(1)

        tweet_id = update(twitter=twitter, status="")
        update(twitter=twitter, status="", tweet_id=tweet_id)
    elif tweet_type == "image":
        table = []
        for chid, subsc in chid_subsc_list:
            prev_subsc = prev_subsc_dict.get(chid)
            # NOTE: not sophisticated
            name = chinfo[chinfo["chid"] == chid]["name"].values[0]
            if prev_subsc is not None:
                diff = subsc - prev_subsc
                if diff != 0:
                    table.append(
                        [f"{name:s}", f"{subsc:,d}", f"{diff:+,d}"]
                    )
                else:
                    table.append(
                        [f"{name:s}", f"{subsc:,d}", "0"]
                    )
            else:
                table.append(
                    [f"{name:s}", f"{subsc:,d}", "-"]
                )
        logger.debug(table)
        # NOTE: japanize_matplotlib is used for matplotlib to display japanese,
        #       but it might be better to set fonts on my own.
        #       reference: https://github.com/uehara1414/japanize-matplotlib
        japanize_matplotlib.japanize()

        # generate a table image
        fig, ax = plt.subplots(1, 1, figsize=(4.0, 4.0))
        ax.axis("off")
        ax.axis("tight")
        colors = [['#D8D8D8' for _ in row] if i % 2 == 1 else ["w" for _ in row] for i, row in enumerate(table)]

        table = ax.table(
            cellText=table,
            colLabels=["名前", "登録者数", "前日比"],
            loc="center",
            cellColours=colors,
            )

        # table settings
        # Reference:
        #   https://matplotlib.org/stable/api/table_api.html#matplotlib.table.Table
        #   https://matplotlib.org/stable/api/table_api.html#matplotlib.table.Cell
        table.auto_set_font_size(False)
        for key, cell in table.get_celld().items():
            row, column = key
            if row == 0:
                cell.set_facecolor('#2F2F2F')
                cell.set_text_props(color='w')
            elif row > 0:
                cell.set_text_props(horizontalalignment="center")
            cell.set_width(0.8*cell.get_width())
            cell.set_height(1.2*cell.get_height())
        table.auto_set_column_width([0])
        plt.tight_layout()
        plt.savefig("table.png", format="png", dpi=400)
        plt.close()

        # upload an image and tweet
        with open("table.png", "rb") as media:
            media_ids = upload(twitter=twitter, media=media)
        update(twitter=twitter, status=timestamp, media_ids=media_ids)
        os.remove("table.png")
    else:
        logger.error(f"tweet_type \"{tweet_type}\" is not supported.")
        sys.exit(1)


if __name__ == "__main__":
    main()
