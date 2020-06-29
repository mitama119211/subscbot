from twitter_auth import twitter
import json


def statuses_update(status, in_reply_to_status_id=None):
    url = "https://api.twitter.com/1.1/statuses/update.json"

    params = {"status": status, "in_reply_to_status_id": in_reply_to_status_id}

    response = twitter.post(url, params=params)

    if response.status_code == 200:
        res_text = json.loads(response.text)

        return res_text["id"]
    else:
        print("Failed. : {:d}".format(response.status_code))
        print("An HTTP error {:d} occurred:\n{:s}".format(response.status_code,
                                                          response.content))
