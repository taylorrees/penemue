from limiter import limiter
from db import DB
from twython import Twython
from credentials import app_key, app_secret, auth_token, auth_secret
from time import time


class Users(object):

    def __init__(self):
        self.UPDATE_INTERVAL = 10

    @limiter("users/lookup")
    def lookup(self, user_id):
        twitter = Twython(app_key, app_secret, auth_token, auth_secret)
        users = twitter.lookup_user(user_id=user_id)

        return users

    def update(self):
        users = DB.users.find()
        users = [user for user in users]
        print("Update Users")

        # archive current users
        print("\t 1) Archiving existing user profiles")
        DB.archive.insert({
            "timestamp": time(),
            "document_type": "users",
            "data": users
        })

        user_ids = [user["id_str"] for user in users]
        updated = []

        print("\t 2) Collecting updated user profiles")
        for i in range(0, len(users), 100):
            # take batches of 100 ids
            user_id = user_ids[i : i + 100]
            updated += self.lookup(user_id)

        # overwite existing users
        print("\t 3) Storing updated user profiles")
        DB.users.remove({})
        DB.users.insert_many(users)

    def start(self, callback):
        while True:
            self.update()
            callback()
            time.sleep(self.UPDATE_INTERVAL)
