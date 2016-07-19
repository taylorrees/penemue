from db import DB
from pprint import pprint
from collections import Counter

def statistics():
    """Count the number of tweets containing links and
    the number of unique links. Get the urls and determine
    the 20 most common urls."""
    
    tweets = [t for t in DB.tweets.find()]
    urls = [h["expanded_url"] for t in tweets for h in t["entities"]["urls"]]
    most_common = Counter(urls).most_common(20)
    most_common = {key: value for (key, value) in most_common}

    return {
        "count_total": len(urls),
        "count_unique": len(set(urls)),
        "urls": set(urls),
        "most_common": most_common
    }
