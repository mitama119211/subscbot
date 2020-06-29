from get_subscribers import get_subscribers
from cid_info import cid_info
from statuses_update import statuses_update
import datetime
import os


LOG_ROOT_PATH = "./subscribers_log/"


def output_log(timestamp, log_filename, cid_subsc_list):
    for cid, subscribers in cid_subsc_list:
        log = timestamp + " {:7d}".format(subscribers)
        log_path = LOG_ROOT_PATH + cid_info[cid]["path"] + log_filename
        if os.path.exists(log_path):
            with open(log_path, "a") as f:
                f.write("\n"+log)
        else:
            with open(log_path, "w") as f:
                f.write(log)


def check_last_subsc(cid_subsc_list):
    lastlog_filename = "last_subscribers.log"

    last_subsc_dict = dict()
    for cid, subscribers in cid_subsc_list:
        lastlog_path = LOG_ROOT_PATH + cid_info[cid]["path"] + lastlog_filename
        if os.path.exists(lastlog_path):
            with open(lastlog_path, "r") as f:
                last_subscribers = int(f.read())
            with open(lastlog_path, "w") as f:
                f.write(str(subscribers))
            last_subsc_dict[cid] = last_subscribers
        else:
            with open(lastlog_path, "w") as f:
                f.write(str(subscribers))

    return last_subsc_dict


def form_name(name):
    return "＿"*(6-len(name)) + name


def main():
    if not os.path.exists(LOG_ROOT_PATH):
        os.mkdir(LOG_ROOT_PATH)
        for value in cid_info.values():
            log_path = LOG_ROOT_PATH + value["path"]
            os.mkdir(log_path)

    dt_now = datetime.datetime.now()
    timestamp = dt_now.strftime("%Y-%m-%d_%H:%M:%S")
    log_filename = dt_now.strftime("%Y%m") + ".log"

    cids = ",".join(cid_info.keys())
    cid_subsc_list = get_subscribers(cids)

    output_log(timestamp, log_filename, cid_subsc_list)

    subsc_list_former = []
    subsc_list_latter = []
    last_subsc_dict = check_last_subsc(cid_subsc_list)
    if last_subsc_dict:
        for i, (cid, subsc) in enumerate(cid_subsc_list):
            if i < len(cid_subsc_list)/2:
                subsc_list_former.append("{:s}: {:_=8,d} ({:+})".format(
                    form_name(cid_info[cid]["name"]), subsc,
                    subsc-last_subsc_dict[cid]))
            else:
                subsc_list_latter.append("{:s}: {:_=8,d} ({:+})".format(
                    form_name(cid_info[cid]["name"]), subsc,
                    subsc-last_subsc_dict[cid]))
    else:
        for i, (cid, subsc) in enumerate(cid_subsc_list):
            if i < len(cid_subsc_list)/2:
                subsc_list_former.append("{:s}: {:_=8,d}".format(
                    form_name(cid_info[cid]["name"]), subsc))
            else:
                subsc_list_latter.append("{:s}: {:_=8,d}".format(
                    form_name(cid_info[cid]["name"]), subsc))

    status_former = timestamp + "\n"
    status_former += "\n".join(subsc_list_former)
    status_latter = "\n".join(subsc_list_latter)

    tweet_id = statuses_update(status_former)
    statuses_update(status_latter, tweet_id)

    print(status_former)
    print(status_latter)


if __name__ == "__main__":
    main()
