"""media module."""
import json

import requests_oauthlib


def upload(
    twitter: requests_oauthlib.oauth1_session.OAuth1Session,
    media: str = None,
):
    """Tweet status.

    Args:
        twitter (requests_oauthlib.oauth1_session.OAuth1Session): Session instance.
        media (str): The raw binary file content being uploaded.

    Return:
        media_id (str): Media id.

    Reference:
        https://developer.twitter.com/en/docs/twitter-api/v1/media/upload-media/api-reference/post-media-upload
    """
    resource_url = "https://upload.twitter.com/1.1/media/upload.json"

    if media is not None:
        files = {"media": media}
    else:
        raise RuntimeError("Please specify media.")

    response = twitter.post(resource_url, files=files)

    if response.status_code == 200:
        res_text = json.loads(response.text)

        return res_text["media_id"]
    else:
        response.raise_for_status()
