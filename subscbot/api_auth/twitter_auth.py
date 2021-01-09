from requests_oauthlib import OAuth1Session
import os

API_KEY = os.environ["API_KEY"]
API_KEY_SECRET = os.environ["API_KEY_SECRET"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]

twitter = OAuth1Session(API_KEY, API_KEY_SECRET,
                        ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
