from db import DB
from pprint import pprint
from collections import Counter

def statistics():
    """Count the number of tweets containing hashtags and
    the number of unique hashtags. Get the hashtags and
    determine the 20 most common hashtags."""

    tweets = [t for t in DB.tweets.find()]
    hashtags = [h["text"] for t in tweets for h in t["entities"]["hashtags"]]
    most_common = Counter(hashtags).most_common(20)
    most_common = {key: value for (key, value) in most_common}

    return {
        "count_total": len(hashtags),
        "count_unique": len(set(hashtags)),
        "hashtags": set(hashtags),
        "most_common": most_common
    }
