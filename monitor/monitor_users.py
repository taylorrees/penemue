from credentials import app_key
from credentials import app_secret
from credentials import auth_token
from credentials import auth_secret
from twython import Twython
from limiter import limiter
from time import time
from db import DB


class MonitorUsers(object):

    def __init__(self):
        cr = [app_key, app_secret, auth_token, auth_secret]
        self.twitter = Twython(*cr)
        self.users = [user for user in DB.users.find()]

    def __archive(self):
        # archive current users
        DB.archive.insert({
            "timestamp": time(),
            "document_type": "users",
            "data": self.users
        })

    def __store(self):
        # overwite existing users
        DB.users.remove({})
        DB.users.insert_many(self.users)

    def __collect(self):
        # collect profiles of all users
        user_ids = [user["id_str"] for user in self.users]
        updated = []

        for i in range(0, len(self.users), 100):
            # take batches of 100 ids
            j = i + 100
            user_id = user_ids[i:j]
            updated += self.lookup(user_id)

    @limiter("users/lookup")
    def lookup(self, user_id):
        # rate limited
        return self.twitter.lookup_user(user_id=user_id)

    def update(self):
        print("Update Users")
        print("\t 1. Archiving")
        self.__archive()
        print("\t 2. Collecting")
        self.__collect()
        print("\t 3. Storing")
        self.__store()
