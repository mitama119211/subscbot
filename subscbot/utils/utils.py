import inspect
import matplotlib.pyplot as plt


def count_characters_for_tweet():
    """Count characters for tweet.

    Reference: https://afila0.com/twitter-character-count/
    """
    pass


def get_own_args(skip_self=False):
    parent_frame = inspect.currentframe().f_back
    info = inspect.getargvalues(parent_frame)

    return {key: info.locals[key] for key in info.args[1 if skip_self else 0:]}

