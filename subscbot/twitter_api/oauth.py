"""OAuth related modules."""
import requests
import sys

from logging import getLogger
from urllib.parse import parse_qsl

import requests_oauthlib


def request_token(
    twitter: requests_oauthlib.oauth1_session.OAuth1Session,
    oauth_callback: str,
):
    """Allow a Consumer application to obtain an OAuth Request Token to request user authorization.

    Args:
        twitter (requests_oauthlib.oauth1_session.OAuth1Session): Session instance.
        oauth_callback (str): The URL to which you are redirected.

    Return:
        linkage_url (str): URL of the linkage page.

    Reference:
        https://developer.twitter.com/en/docs/authentication/api-reference/request_token
    """
    # set logger
    logger = getLogger(__name__)

    resource_url = "https://api.twitter.com/oauth/request_token"

    params = {"oauth_callback": oauth_callback}

    response = twitter.post(resource_url, params=params)

    try:
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(e)
        sys.exit(1)

    request_token = dict(parse_qsl(response.content.decode("utf-8")))
    oauth_token = request_token["oauth_token"]
    authenticate_url = "https://api.twitter.com/oauth/authenticate"

    return f"{authenticate_url}?oauth_token={oauth_token}"


def access_token(
    twitter: requests_oauthlib.oauth1_session.OAuth1Session,
    oauth_verifier: str,
):
    """Allow a Consumer application to obtain an OAuth Request Token to request user authorization.

    Args:
        twitter (requests_oauthlib.oauth1_session.OAuth1Session): Session instance.
        oauth_verifier (str): oauth verifier.

    Return:
        access_token_ (dict): Token dict including ACCESS_TOKEN and ACCESS_TOKEN_SECRET.

    Reference:
        https://developer.twitter.com/en/docs/authentication/api-reference/access_token
    """
    # set logger
    logger = getLogger(__name__)

    resource_url = "https://api.twitter.com/oauth/access_token"

    params = {"oauth_verifier": oauth_verifier}

    response = twitter.post(resource_url, params=params)

    try:
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(e)
        sys.exit(1)

    content = dict(parse_qsl(response.content.decode("utf-8")))

    return {"ACCESS_TOKEN": content["oauth_token"], "ACCESS_TOKEN_SECRET": content["oauth_token_secret"]}
