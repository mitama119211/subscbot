import json

# from utils import *
from subscbot.api_auth import twitter


def statuses_update(
    status,
    in_reply_to_status_id="",
    auto_papulate_reply_metadata=False,
    exclude_reply_user_ids="",
    attachment_url="",
    media_ids="",
    possibly_sensitive=False,
    lat="",
    long="",
    place_id="",
    display_coordinates="",
    trim_user=False,
    enable_dmcommands=False,
    fail_dmcommands=True,
    card_uri="",
):
    url = "https://api.twitter.com/1.1/statuses/update.json"

    params = {"status": status, "in_reply_to_status_id": in_reply_to_status_id, "media_ids": media_ids}

    response = twitter.post(url, params=params)

    if response.status_code == 200:
        res_text = json.loads(response.text)

        return res_text["id"]
    else:
        print("Failed. : {:d}".format(response.status_code))
        print(
            "An HTTP error {:d} occurred:\n{:s}".format(
                response.status_code, response.content
            )
        )
