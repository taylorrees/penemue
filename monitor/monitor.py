from db import DB
from stream import Stream
from credentials import app_key, app_secret, auth_token, auth_secret


class Stream(Stream):

    def on_success(self, tweet):
        # extend stream
        # on_success add tweet to db
        DB.tweets.insert(tweet)
        print("\t id_str: %s" % tweet["id_str"])


class Monitor(object):

    def __init__(self):
        self.stream = Stream(app_key, app_secret, auth_token, auth_secret)

    def start(self):
        # comma separated user ids
        users = DB.users.find()
        users = [user["id_str"] for user in users]
        users = ",".join(users)

        # start stream
        print("Starting stream...")
        self.stream.statuses.filter(follow=users, language="en")

    def stop(self):
        # end stream
        self.stream.disconnect()
        print("Ending stream...")

    def restart(self):
        self.stop()
        self.start()
