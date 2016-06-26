import json
import time
import credentials as c
from twython import Twython


class Collect(object):
    """
    A small class for collecting and storing a list of
    Twitter user profiles retrieved from specific Twitter lists.
    The Twitter lists can be specified using URLs of the
    lists, from which the necessary arguments will be extracted.
    Such arguments would be the list slug and user screen name.
    """

    def __init__(self, lists):
        """
        Where the list of Twitter list URLs should be specified.

        @constructor
        @param {Str} url
        """

        # remove duplicates
        urls = list(set(lists))

        self.twitter = Twython(c.app_key, c.app_secret,
                               c.auth_token, c.auth_secret)
        self.urls = []
        self.members = []
        stopwords = ["", "https:", "twitter.com"]

        for url in urls:
            self.urls.append({
                "url": url,
                "args": [level for level in url.split("/") if level not in stopwords]
            })

    def rate_limit(self):
        """
        A far too simple rate limiter, to try and prevent the
        number of requests exceeding the API limit.
        """

        req = 12
        per = 60

        # Needs improvement
        print('.')
        wait = 1 / (req / per)
        time.sleep(wait)

    def remove_duplicate_members(self):
        """
        Remove duplicated user profiles from the list of
        members.
        """

        ids = set()
        filtered = []
        duplicates = 0

        for user in self.members:
            if user["id_str"] not in ids:
                ids.add(user["id_str"])
                filtered.append(user)

        self.members = filtered

        duplicates = len(self.members) - len(filtered)
        print("Duplicates removed: %s" % duplicates)

    def get_members(self):
        """
        Creates a list of Twitter user profiles who are members of
        the specified lists.

        See: https://dev.twitter.com/rest/reference/get/lists/members

        @return {list of strings}
        """

        for url in self.urls:
            twitter_list = self.twitter.get_list_members(
                slug=url["args"][2], owner_screen_name=url["args"][0], count=5000)
            # sleep after request
            self.rate_limit()
            users = [member for member in twitter_list["users"]]
            self.members += users

        self.remove_duplicate_members()

        print("Users: %s" % len(self.members))
        return self.members

    def to_json_file(self, path):
        """
        Stores the users in a JSON file specified by the path
        parameter.

        @param {string} path
        """

        with open(path, "w") as outfile:
            json.dump(self.get_members(), outfile)
            outfile.close()


if __name__ == "__main__":
    start = time.time()

    print("Starting...")

    with open("../json/twitter_lists.json") as infile:
        lists = json.load(infile)
        collector = Collect(lists)
        collector.to_json_file("../json/twitter_profiles.json")
        infile.close()

    print("Finished")
    print("Duration: %.2fs" % (time.time() - start))
