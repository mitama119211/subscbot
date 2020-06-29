from cid_info import cid_info
from get_subscribers import get_subscribers
from statuses_update import statuses_update
import datetime
import os

NOTIFY_CRITERION = 10000
ROUNDNUMBER = 1000
RNLOG_ROOT_PATH = "./roundnumber_log/"


def init_rnlog():
    os.mkdir(RNLOG_ROOT_PATH)
    for value in cid_info.values():
        rnlog_path = RNLOG_ROOT_PATH + value["path"]
        os.mkdir(rnlog_path)


def remaining(diff):
    if 0 < diff <= 10:
        return 10
    elif 10 < diff <= 50:
        return 50
    elif 50 < diff <= 100:
        return 100
    else:
        return -1


def check_notified(cid_subsc_list, init_flag):
    notifiednum_filename = "notifyied_number.log"

    notify_list = []
    if init_flag:
        for cid, subscribers in cid_subsc_list:
            notifiednum_path = RNLOG_ROOT_PATH + cid_info[cid]["path"] + notifiednum_filename
            next_criterion = (subscribers//NOTIFY_CRITERION + 1) * NOTIFY_CRITERION
            diff = next_criterion - subscribers
            remain = remaining(diff)

            with open(notifiednum_path, "w") as f:
                if remain == -1:
                    f.write(str(subscribers//NOTIFY_CRITERION * NOTIFY_CRITERION))
                else:
                    f.write(str(next_criterion-remain))
    else:
        for cid, subscribers in cid_subsc_list:
            notifiednum_path = RNLOG_ROOT_PATH + cid_info[cid]["path"] + notifiednum_filename
            next_criterion = (subscribers//NOTIFY_CRITERION + 1) * NOTIFY_CRITERION
            diff = next_criterion - subscribers
            remain = remaining(diff)

            with open(notifiednum_path, "r") as f:
                last_notifiednum = int(f.read())

            if remain == -1:
                continue
            else:
                if last_notifiednum < next_criterion-remain:
                    notify_list.append((cid, next_criterion, diff))
                    with open(notifiednum_path, "w") as f:
                        f.write(str(next_criterion-remain))
                else:
                    continue

    return notify_list


def check_roundnumber(cid_subsc_list, init_flag):
    roundnumber_filename = "roundnumber.log"

    roundnumber_list = []
    if init_flag:
        for cid, subscribers in cid_subsc_list:
            roundnum_path = RNLOG_ROOT_PATH + cid_info[cid]["path"] + roundnumber_filename
            reached_roundnumber = subscribers//ROUNDNUMBER * ROUNDNUMBER
            with open(roundnum_path, "w") as f:
                f.write(str(reached_roundnumber))
    else:
        for cid, subscribers in cid_subsc_list:
            roundnum_path = RNLOG_ROOT_PATH + cid_info[cid]["path"] + roundnumber_filename
            reached_roundnumber = subscribers//ROUNDNUMBER * ROUNDNUMBER

            with open(roundnum_path, "r") as f:
                last_roundnumber = int(f.read())

            if last_roundnumber < reached_roundnumber:
                roundnumber_list.append((cid, reached_roundnumber, subscribers))
                with open(roundnum_path, "w") as f:
                    f.write(str(reached_roundnumber))
            else:
                continue

    return roundnumber_list


def notify_status(timestamp, cid, next_criterion, diff):
    status = timestamp + "\n"
    status += "#" + cid_info[cid]["name"] + " さんのチャンネル登録者数{:,d}人まで".format(next_criterion)
    status += "残り{:,d}人です。".format(diff)

    return status


def roundnumber_status(timestamp, cid, reached_roundnumber, subscribers):
    status = timestamp + "\n"
    status += "#" + cid_info[cid]["name"] + " さんのチャンネル登録者数が"
    status += "{:,d}人を達成しました！\n".format(reached_roundnumber)
    status += "現在: {:,d}人".format(subscribers)

    return status


def main():
    dt_now = datetime.datetime.now()
    timestamp = dt_now.strftime("%Y-%m-%d_%H:%M:%S")

    # チャンネル登録者数取得
    cids = ",".join(cid_info.keys())
    cid_subsc_list = get_subscribers(cids)

    if not os.path.exists(RNLOG_ROOT_PATH):
        init_rnlog()
        init_flag = True
        print("Initialized.")
    else:
        init_flag = False

    notify_list = check_notified(cid_subsc_list, init_flag)
    roundnumber_list = check_roundnumber(cid_subsc_list, init_flag)

    if not init_flag:
        status_list = []
        for cid, next_criterion, diff in notify_list:
            status_list.append(notify_status(timestamp, cid, next_criterion, diff))
        for cid, reached_roundnumber, subscribers in roundnumber_list:
            status_list.append(roundnumber_status(timestamp, cid, reached_roundnumber, subscribers))
        for status in status_list:
            print(status)
            statuses_update(status)


if __name__ == "__main__":
    main()
