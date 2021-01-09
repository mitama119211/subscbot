"""Generate ACCESS_TOKEN and ACCESS_TOKEN_SECRET."""
import argparse
import os

from urllib.parse import parse_qsl

from requests_oauthlib import OAuth1Session

from subscbot.twitter_api import access_token
from subscbot.twitter_api import request_token


def get_arguments():
    """Get arguments."""
    parser = argparse.ArgumentParser(
        description="Generate ACCESS_TOKEN and ACCESS_TOKEN_SECRET.")
    parser.add_argument("--oauth_callback", type=str, required=True,
                        help="One of the Callback URLs configured in the Twitter App.")
    return parser.parse_args()


def main():
    """Generate tokens."""
    # get argumments
    args = get_arguments()

    # get API_KEY and API_KEY_SECRET
    API_KEY = os.environ.get("API_KEY")
    API_KEY_SECRET = os.environ.get("API_KEY_SECRET")

    if API_KEY is None or API_KEY_SECRET is None:
        raise RuntimeError("API_KEY and API_KEY_SECRET must be specified in environment variables.")

    twitter = OAuth1Session(API_KEY, API_KEY_SECRET)

    # generate linkage url
    linkage_url = request_token(twitter=twitter, oauth_callback=args.oauth_callback)
    print(f"Please access the following URL: {linkage_url}")
    print("After you have allowed access to the app,"
          "enter the redirected URL of the form \"https://example.com?oauth_token=XXX&oauth_verifier=YYY\".")
    callback = input("URL: ")

    # generate access token
    tokens = dict(parse_qsl(callback.split("?")[1]))
    oauth_token = tokens["oauth_token"]
    oauth_verifier = tokens["oauth_verifier"]
    twitter = OAuth1Session(API_KEY, API_KEY_SECRET, oauth_token, oauth_verifier)
    access_token_ = access_token(twitter=twitter, oauth_verifier=oauth_verifier)
    print(f"ACCESS_TOKEN: {access_token_['ACCESS_TOKEN']}")
    print(f"ACCESS_TOKEN_SECRET: {access_token_['ACCESS_TOKEN_SECRET']}")


if __name__ == "__main__":
    main()
