"""Statuses module."""
import json

import requests_oauthlib


def update(
    twitter: requests_oauthlib.oauth1_session.OAuth1Session,
    status: str,
    in_reply_to_status_id: str = "",
    media_ids: str = "",
):
    """Tweet status.

    Args:
        twitter (requests_oauthlib.oauth1_session.OAuth1Session): Session instance.
        status (str): Text of tweet.
        in_reply_to_status_id (str): Tweet id in reply to.
        media_ids (str): Media id to upload.

    Return:
        status_id (str): Tweet id.

    Reference:
        https://developer.twitter.com/en/docs/twitter-api/v1/tweets/post-and-engage/api-reference/post-statuses-update
    """
    resource_url = "https://api.twitter.com/1.1/statuses/update.json"

    params = {"status": status, "in_reply_to_status_id": in_reply_to_status_id, "media_ids": media_ids}

    response = twitter.post(resource_url, params=params)

    if response.status_code == 200:
        res_text = json.loads(response.text)

        return res_text["id"]
    else:
        response.raise_for_status()
