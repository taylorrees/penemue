import sys
import json

tweets_file = '../data/output/tweets.json'


def __report(n, tweet):
    """Report on function progress"""

    if n % 1000 == 0:
        sys.stdout.write("=")
        sys.stdout.flush()

    return tweet


def twiterate(callback, tweets_file=tweets_file, *args, **kwargs):
    """Iterate through tweets"""

    sys.stdout.write("[Progress] \n[")
    sys.stdout.flush()

    with open(tweets_file, "r") as tweets:
        result = [callback(__report(n, json.loads(tweet)), *args, **kwargs)
                for n, tweet in enumerate(tweets)
                    if callback(json.loads(tweet), *args, **kwargs)]

    sys.stdout.write("]\n")
    sys.stdout.flush()

    return result
