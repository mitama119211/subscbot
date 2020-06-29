from youtube_auth import youtube
from googleapiclient.errors import HttpError
from operator import itemgetter


def get_subscribers(cids):
    channels_response = youtube.channels().list(
                                          part="id,snippet,statistics",
                                          id=cids
                                         ).execute()
    try:
        items = channels_response.get("items", [])
    except HttpError as e:
        print("An HTTP error {:d} occurred:\n{:s}".format(e.resp.status,
                                                          e.content))

    cid_subsc_list = []
    for item in items:
        cid = item["id"]
        subscribers = int(item["statistics"]["subscriberCount"])
        cid_subsc_list.append((cid, subscribers))

    cid_subsc_list = sorted(cid_subsc_list, key=itemgetter(1), reverse=True)

    return cid_subsc_list
