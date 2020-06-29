from statuses_update import statuses_update
import datetime
import os


def main():
    status_filename = "status.txt"
    dt_now = datetime.datetime.now()
    timestamp = dt_now.strftime("%Y-%m-%d_%H:%M:%S")

    if os.path.exists(status_filename):
        status = timestamp + "\n"
        with open(status_filename, "r", encoding="utf-8") as f:
            status += f.read()
        if statuses_update(status):
            os.remove(status_filename)
    else:
        print("There is not {:s}.".format(status_filename))


if __name__ == "__main__":
    main()
