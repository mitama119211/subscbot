from operator import itemgetter

import pandas as pd

from googleapiclient.errors import HttpError

from subscbot.api_auth import youtube


def get_subscribers(chids):
    channels_response = youtube.channels().list(
                                          part="id,snippet,statistics",
                                          id=chids
                                         ).execute()
    try:
        items = channels_response.get("items", [])
    except HttpError as e:
        print("An HTTP error {:d} occurred:\n{:s}".format(e.resp.status,
                                                          e.content))

    chid_subsc_list = []
    for item in items:
        chid = item["id"]
        subscribers = int(item["statistics"]["subscriberCount"])
        chid_subsc_list.append([chid, subscribers])

    chid_subsc_list = sorted(chid_subsc_list, key=itemgetter(1), reverse=True)

    return chid_subsc_list
