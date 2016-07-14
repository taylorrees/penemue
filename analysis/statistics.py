from pymongo import MongoClient
from json import load
from collect import Collect
from db import DB
from pprint import pprint


class Collect(Collect):
    def store(self, collection):
        # extend and alter store
        DB[collection].delete_many({})
        DB[collection].insert_many(self.members)


def get():
    """Get the number of users, tweets, original tweets, retweets
    and replies for all users, journalists, organisations and users
    external to the study"""

    get & store journalists from twitter lists
    j = load(open("journalists.json"))
    collect = Collect(lists=j)
    collect.store("journalists")

    # get & store news organisations from twitter lists
    o = load(open("organisations.json"))
    collect = Collect(lists=o, refine=False, append=True)
    collect.store("organisations")

    # get sets of id_str's
    journalists = DB.journalists.distinct("id_str")
    organisations = DB.organisations.distinct("id_str")

    # used to collect results
    stats = {
        "all": {}, # all
        "joi": {}, # journalists of interest
        "ooi": {}, # organisations of interest
        "ext": {}  # external
    }


    # -- ALL --
    # -- All Accounts --
    # All tweets stored within the tweets collection.
    # This provides a base figure to work from.

    stats["all"]["users"] = len(journalists + organisations)

    stats["all"]["total"] = DB.tweets.find().count()

    stats["all"]["originals"] = DB.tweets.find({
        "in_reply_to_status_id_str": {"$eq": None},
        "retweeted_status": {"$exists": False}
    }).count()

    stats["all"]["retweets"] = DB.tweets.find({
        "retweeted_status": {"$exists": True}
    }).count()

    stats["all"]["replies"] = DB.tweets.find({
        "in_reply_to_status_id_str": {"$ne": None}
    }).count()


    # -- JOI --
    # -- Journalists of Interest --
    # Those tweets created by the list of journalists
    # provided to the streaming follow parameter.

    stats["joi"]["users"] = len(journalists)

    stats["joi"]["total"] = DB.tweets.find({
        "user.id_str": {"$in": journalists}
    }).count()

    stats["joi"]["originals"] = DB.tweets.find({
        "user.id_str": {"$in": journalists},
        "in_reply_to_status_id_str": {"$eq": None},
        "retweeted_status": {"$exists": False}
    }).count()

    stats["joi"]["retweets"] = DB.tweets.find({
        "user.id_str": {"$in": journalists},
        "retweeted_status": {"$exists": True}
    }).count()

    stats["joi"]["replies"] = DB.tweets.find({
        "user.id_str": {"$in": journalists},
        "in_reply_to_status_id_str": {"$ne": None}
    }).count()


    # -- OOI --
    # -- Organisations of Interest --
    # Those tweets created by the list of organisations
    # provided to the streaming follow parameter.

    stats["ooi"]["users"] = len(organisations)

    stats["ooi"]["total"] = DB.tweets.find({
        "user.id_str": {"$in": organisations}
    }).count()

    stats["ooi"]["originals"] = DB.tweets.find({
        "user.id_str": {"$in": organisations},
        "in_reply_to_status_id_str": {"$eq": None},
        "retweeted_status": {"$exists": False}
    }).count()

    stats["ooi"]["retweets"] = DB.tweets.find({
        "user.id_str": {"$in": organisations},
        "retweeted_status": {"$exists": True}
    }).count()

    stats["ooi"]["replies"] = DB.tweets.find({
        "user.id_str": {"$in": organisations},
        "in_reply_to_status_id_str": {"$ne": None}
    }).count()


    # -- EXT --
    # -- External Accounts --
    # Those tweets created created by any user not
    # provided to the streaming follow parameter.

    stats["ext"]["users"] = DB.tweets.count() - len((journalists + organisations))

    stats["ext"]["total"] = DB.tweets.find({
        "user.id_str": {"$nin": (journalists + organisations)}
    }).count()

    stats["ext"]["originals"] = DB.tweets.find({
        "user.id_str": {"$nin": (journalists + organisations)},
        "in_reply_to_status_id_str": {"$eq": None},
        "retweeted_status": {"$exists": False}
    }).count()

    stats["ext"]["retweets"] = DB.tweets.find({
        "user.id_str": {"$nin": (journalists + organisations)},
        "retweeted_status": {"$exists": True}
    }).count()

    stats["ext"]["replies"] = DB.tweets.find({
        "user.id_str": {"$nin": (journalists + organisations)},
        "in_reply_to_status_id_str": {"$ne": None}
    }).count()


    return stats
