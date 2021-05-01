"""Generate ACCESS_TOKEN and ACCESS_TOKEN_SECRET."""
import argparse
import sys

from logging import basicConfig
from logging import getLogger
from urllib.parse import parse_qsl

import yaml

from requests_oauthlib import OAuth1Session

from subscbot.twitter_api import access_token
from subscbot.twitter_api import request_token


def get_arguments():
    """Get arguments."""
    parser = argparse.ArgumentParser(
        description="Generate ACCESS_TOKEN and ACCESS_TOKEN_SECRET.")
    parser.add_argument("--conf", type=str, default="conf/config.yaml",
                        help="Path to a config file with API keys.")
    parser.add_argument("--oauth_callback", type=str, required=True,
                        help="One of the Callback URLs configured in the Twitter App.")
    parser.add_argument("--verbose", type=int, default=1,
                        help="Logging level.")
    return parser.parse_args()


def main():
    """Generate tokens."""
    # get argumments
    args = get_arguments()

    # set logger
    if args.verbose > 1:
        from logging import DEBUG
        basicConfig(
            level=DEBUG, stream=sys.stdout,
            format="%(asctime)s (%(module)s:%(lineno)d) %(levelname)s: %(message)s")
    elif args.verbose == 1:
        from logging import INFO
        basicConfig(
            level=INFO, stream=sys.stdout,
            format="%(asctime)s (%(module)s:%(lineno)d) %(levelname)s: %(message)s")
    else:
        from logging import WARN
        basicConfig(
            level=WARN, stream=sys.stdout,
            format="%(asctime)s (%(module)s:%(lineno)d) %(levelname)s: %(message)s")
    logger = getLogger(__name__)

    # load config
    with open(args.conf, mode="r") as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)

    # get API keys
    api_keys = config.get("api_keys", "")
    try:
        API_KEY = api_keys["API_KEY"]
        API_KEY_SECRET = api_keys["API_KEY_SECRET"]
    except KeyError:
        logger.error("API keys must be specified.")
        sys.exit(1)
    if not all(api_keys.values()):
        logger.error("API keys must be specified.")
        sys.exit(1)

    # launch a session
    twitter = OAuth1Session(API_KEY, API_KEY_SECRET)

    # generate linkage url
    linkage_url = request_token(twitter=twitter, oauth_callback=args.oauth_callback)
    logger.info(f"Please access the following URL: {linkage_url}")
    logger.info("After you have allowed access to the app, "
                "enter the redirected URL of the form \"https://example.com?oauth_token=XXX&oauth_verifier=YYY\".")
    callback = input("URL: ")

    # generate access token
    tokens = dict(parse_qsl(callback.split("?")[1]))
    oauth_token = tokens["oauth_token"]
    oauth_verifier = tokens["oauth_verifier"]
    twitter = OAuth1Session(API_KEY, API_KEY_SECRET, oauth_token, oauth_verifier)
    access_token_ = access_token(twitter=twitter, oauth_verifier=oauth_verifier)
    logger.info(f"ACCESS_TOKEN: \"{access_token_['ACCESS_TOKEN']}\"")
    logger.info(f"ACCESS_TOKEN_SECRET: \"{access_token_['ACCESS_TOKEN_SECRET']}\"")


if __name__ == "__main__":
    main()
