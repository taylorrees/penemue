from credentials import app_key
from credentials import app_secret
from credentials import auth_token
from credentials import auth_secret
from twython import Twython
from limiter import limiter
from .filter import remove_duplicate_users
from .filter import refine
from db import DB


class Collect(object):
    """Get, merge and filter the members of the provided Twitter lists."""

    def __init__(self, lists):
        """
        :param lists: a python list of twitter list urls
        """

        urls = list(set(lists)) # remove duplicates
        stopwords = ["", "https:", "twitter.com"]
        cr = [app_key, app_secret, auth_token, auth_secret]

        self.twitter = Twython(*cr)
        self.urls = []

        for url in urls:
            args = [arg for arg in url.split("/") if arg not in stopwords]
            self.urls.append({"url": url, "args": args})

        self.members = self.__members()

    def __members(self):
        """Get and merge all members of the provided Twitter lists."""

        print("Collecting...")
        users = []

        for url in self.urls:
            slug = url["args"][2]
            owner = url["args"][0]
            args = {"slug": slug, "owner_screen_name": owner, "count": 5000}
            members = self.__list_members(**args)
            users += [member for member in members["users"]]

        # filter users
        users = remove_duplicate_users(users)
        users = refine(users)

        return users

    @limiter("lists/members")
    def __list_members(self, *args, **kwargs):
        """Twython method wrapper, to envoke rate limiter."""

        return self.twitter.get_list_members(**kwargs)

    def store(self):
        """Store the users from the lists to the database."""

        DB.users.remove({})
        DB.users.insert_many(self.members)
