"""Issue ACCESS_TOKEN and ACCESS_TOKEN_SECTET."""

import argparse
import os

from requests_oauthlib import OAuth1Session
from urllib.parse import parse_qsl


def request_token(
    oauth_callback,
):
    resource_url = "https://api.twitter.com/oauth/request_token"

    params = {"oauth_callback": oauth_callback}

    twitter = OAuth1Session(API_KEY, API_KEY_SECRET)
    response = twitter.post(resource_url, params=params)

    if response.status_code == 200:
        request_token = dict(parse_qsl(response.content.decode("utf-8")))
        oauth_token = request_token["oauth_token"]
        authenticate_url = "https://api.twitter.com/oauth/authenticate"

        return f"{authenticate_url}?oauth_token={oauth_token}"
    else:
        print("Failed. : {:d}".format(response.status_code))
        print(
            "An HTTP error {:d} occurred:\n{:s}".format(
                response.status_code, response.content
            )
        )


def access_token(oauth_token, oauth_verifier):
    resource_url = "https://api.twitter.com/oauth/access_token"

    params = {"oauth_verifier": oauth_verifier}

    twitter = OAuth1Session(API_KEY, API_KEY_SECRET, oauth_token, oauth_verifier)
    response = twitter.post(resource_url, params=params)

    if response.status_code == 200:
        access_token = dict(parse_qsl(response.content.decode("utf-8")))

        return access_token
    else:
        print("Failed. : {:d}".format(response.status_code))
        print(
            "An HTTP error {:d} occurred:\n{:s}".format(
                response.status_code, response.content
            )
        )


def main():
    """."""
    # get argumments
    parser = argparse.ArgumentParser()
    parser.add_argument("--ouath_callback", type=str, default="http://twitter.com")
    args = parser.parse_args()

    API_KEY = os.environ.get("API_KEY")
    API_KEY_SECRET = os.environ.get("API_KEY_SECRET")

    if API_KEY is None or API_KEY_SECRET is None:
        raise RuntimeError("API_KEY and API_KEY_SECRET must be specified in environment variables.")

    # generate oauth url
    print(request_token(oauth_callback=args.oauth_callback))
    callback = input("callback: ")
    oauth = dict(parse_qsl(callback.split("?")[1]))
    print(access_token(**oauth))


if __name__ == "__main__":
    main()
