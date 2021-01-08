import json

from subscbot.api_auth import twitter


def media_upload(
    media=None,
    media_data=None,
):
    url = "https://upload.twitter.com/1.1/media/upload.json"

    if media is not None:
        files = {"media": media}
    elif media_data is not None:
        files = {"media_data": media_data}

    response = twitter.post(url, files=files)

    if response.status_code == 200:
        res_text = json.loads(response.text)

        return res_text["media_id"]
    else:
        print("Failed. : {:d}".format(response.status_code))
        print(
            "An HTTP error {:d} occurred:\n{:s}".format(
                response.status_code, response.content
            )
        )
