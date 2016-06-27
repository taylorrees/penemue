import json
import words
import time


def has_keyword(text):
    """
    Check for presence of keyword in text.
    """

    for word in words.keywords:
        if word in text.lower():
            return True

    return False


def is_active(user, days=10):
    """
    Check user activity for specified number of days.
    """

    # days in seconds
    seconds = lambda days : days * 24 * 60 * 60

    if "status" in user:
        # get created_at attribute
        # convert to seconds
        created_at = user["status"]["created_at"]
        created_at = time.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")
        created_at = time.mktime(created_at)

        now = time.time()
        active_since = now - seconds(days=days)

        if created_at > active_since:
            return True

        return False


if __name__ == "__main__":

    filtered = []

    with open("../json/twitter_profiles.json") as infile:
        users = json.load(infile)
        infile.close()

    for user in users:
        if has_keyword(user["description"]) and (not user["protected"]) and is_active(user):
            filtered.append(user)

    with open("../json/twitter_profiles.json", "w") as outfile:
        json.dump(filtered, outfile)
        outfile.close()

    print("Users: %s" % len(users))
    print("Filtered: %s" % len(filtered))
    
