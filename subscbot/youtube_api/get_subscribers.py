"""Get the number of subscribers."""
from operator import itemgetter

import googleapiclient


def get_subscribers(
    youtube: googleapiclient.discovery.Resource,
    chids: str
):
    """Get the number of subscribers.

    Args:
        youtube (googleapiclient.discovery.Resource): Sesstion instance.
        chids (str): Youtube channel IDs.

    Return:
        chid_subsc_list (list): 2D-list including ["chid", "subscribers"]
    """
    channels_response = youtube.channels().list(
                                          part="id,snippet,statistics",
                                          id=chids
                                         ).execute()

    items = channels_response.get("items", [])

    chid_subsc_list = []
    for item in items:
        chid = item["id"]
        subscribers = int(item["statistics"]["subscriberCount"])
        chid_subsc_list.append([chid, subscribers])

    chid_subsc_list = sorted(chid_subsc_list, key=itemgetter(1), reverse=True)

    return chid_subsc_list
