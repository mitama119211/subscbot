"""Tweet the number of subscribers with text or an image."""
import argparse
import datetime
import logging
import os

import japanize_matplotlib
import matplotlib.pyplot as plt
import pandas as pd

from subscbot.twitter_api import media_upload
from subscbot.twitter_api import statuses_update
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


def check_prev_subsc(chid_subsc_list, chinfo):
    """Check the previous log."""
    # set previous log file name
    # FIXME: avoid hard-coding
    prevlog_filename = "prev_subscribers.log"

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
    parser.add_argument("--chinfo", type=str, default="chinfo.csv")
    parser.add_argument("--log_root_path", type=str, default="subscribers_log")
    parser.add_argument("--tweet_type", type=str, default="image")

    return parser.parse_args()


def main():
    """Tweet the number of subscribers with text or an image."""
    # get arguments
    args = get_arguments()

    # load channel info
    # chinfo: (chid, name, dirname)
    chinfo = pd.read_csv(args.chinfo)

    # check log dirctory existance
    log_root_path = args.log_root_path
    if not os.path.exists(log_root_path):
        os.makedirs(log_root_path)
    log_path_list = [os.path.join(log_root_path, dirname) for dirname in chinfo["dirname"]]
    chinfo["log_path"] = log_path_list
    for log_path in log_path_list:
        if not os.path.exists(log_path):
            os.mkdir(log_path)

    # get current time
    datetime_now = datetime.datetime.now()
    # set timestamp (YYYY-MM-DD_hh:mm:ss)
    timestamp = datetime_now.strftime("%Y-%m-%d_%H:%M:%S")

    # get the number of subscribers
    chids = ",".join(chinfo["chid"])
    chid_subsc_list = get_subscribers(chids)
    # chid_subsc_list = [['UCLhUvJ_wO9hOvv_yYENu4fQ', 697000], ['UCz6Gi81kE6p5cdW1rT0ixqw', 153000], ['UC5nfcGkOAm3JwfPvJvzplHg', 111000], ['UCiGcHHHT3kBB1IGOrv7f3qQ', 105000], ['UC6TyfKcsrPwBsBnx2QobVLQ', 104000], ['UC1519-d1jzGiL1MPTxEdtSA', 103000], ['UCP9ZgeIJ3Ri9En69R0kJc9Q', 95500], ['UCyb-cllCkMREr9de-hoiDrg', 87100], ['UCUZ5AlC3rTlM-rA2cj5RP6w', 86900], ['UCMzxQ58QL4NNbWghGymtHvw', 82500], ['UCju7v8SkoWUQ5ITCQwmYpYg', 73600], ['UCAZ_LA7f0sjuZ1Ni8L2uITw', 67000], ['UCmM5LprTu6-mSlIiRNkiXYg', 64100], ['UCKUcnaLsG2DeQqza8zRXHiA', 59200], ['UCcd4MSYH7bPIBEUqmBgSZQw', 4160], ['UCSlcMof1GIPvH6H_VcknCbQ', 4150], ['UCtM5G3bS7zM8bv6p-OwoNTw', 4140]]

    # output logs of the number of subscribers
    output_log(datetime_now, chid_subsc_list, chinfo=chinfo)

    # tweet the number of subscribers
    tweet_type = args.tweet_type
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

        tweet_id = statuses_update("")
        statuses_update("", tweet_id)
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
        # NOTE: japanize_matplotlib is used for matplotlib to display japanese,
        #       but it might be better to set fonts on my own.
        #       reference: https://github.com/uehara1414/japanize-matplotlib
        japanize_matplotlib.japanize()

        # generate a table image
        fig, ax = plt.subplots(1, 1)
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
        table.auto_set_font_size(False)
        for key, cell in table.get_celld().items():
            row, column = key
            if row == 0:
                cell.set_facecolor('#2F2F2F')
                cell.set_text_props(color='w')
            elif row > 0:
                cell.set_text_props(horizontalalignment="center")
            cell.set_width(0.6*cell.get_width())
            cell.set_height(1.2*cell.get_height())

        plt.tight_layout()
        plt.savefig("table.png", format="png", dpi=400)
        plt.close()

        # upload an image and tweet
        with open("table.png", "rb") as media:
            media_ids = media_upload(media=media)
        statuses_update(status=timestamp, media_ids=media_ids)
        os.remove("table.png")
    else:
        raise RuntimeError(f"tweet_type \"{tweet_type}\" is not supported.")


if __name__ == "__main__":
    main()
