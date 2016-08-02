from time import time
from time import strptime
from time import mktime

from .config import db

keywords = [
    "broadcaster",
    "journalists",
    "editor",
    "hack",
    "sub",
    "critic",
    "reporter",
    "journo",
    "commentator",
    "journalist",
    "columnist",
    "correspondent",
    "presenter",
    "producer",
    "features",
    "writing"
]


def user_has_keyword(user):
    """Check for presence of keyword in user description.

    :param user: a twitter user object
    """

    for word in keywords:
        if word in user["description"].lower():
            return True

    return False


def user_is_active(user, days=30):
    """Check user activity for specified number of days.

    :param user: a twitter user object
    :param days: integer
    """

    # days in seconds
    seconds = lambda days: days * 24 * 60 * 60

    if "status" in user:
        # get created_at attribute
        # convert to seconds
        created_at = user["status"]["created_at"]
        created_at = strptime(created_at, "%a %b %d %H:%M:%S %z %Y")
        created_at = mktime(created_at)

        now = time()
        active_since = now - seconds(days=days)

        if created_at > active_since:
            return True

        return False


def user_is_public(user):
    """Check if the user has a public account.

    :param user: a twitter user object
    """

    return not user["protected"]


def remove_duplicate_users(users):
    """Check for duplicated users and remove.

    :param users: a list of twitter user object
    """

    ids = set()
    filtered = []

    for user in users:
        if user["id_str"] not in ids:
            ids.add(user["id_str"])
            filtered.append(user)

    return filtered


def refine(users):
    """Filter list of users according to specified criteria.

    :param users: a list of twitter user object
    """

    filtered = []

    for user in users:
        if user_has_keyword(user) and user_is_public(user) and user_is_active(user):
            filtered.append(user)

    print("Filtered: %s" % len(filtered))

    return filtered
