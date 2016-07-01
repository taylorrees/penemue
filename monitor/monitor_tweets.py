from credentials import app_key
from credentials import app_secret
from credentials import auth_token
from credentials import auth_secret
from twython import TwythonStreamer
from time import sleep
from db import DB


class Stream(TwythonStreamer):

    def on_success(self, tweet):
        """Store tweet when received."""
        # extend stream
        # on_success add tweet to db
        DB.tweets.insert(tweet)

    def on_error(self, status_code, data):
        """Handle streaming error."""
        print(status_code)
        return True

    def on_timeout(self):
        """Handle request timeout."""
        print("Timeout...")
        return True


class MonitorTweets(object):

    def __init__(self):
        cr = [app_key, app_secret, auth_token, auth_secret]
        self.stream = Stream(*cr)

    def start(self):
        """Start the twitter stream."""

        # comma separated user ids
        users = DB.users.find()
        users = [user["id_str"] for user in users]
        users = ",".join(users)

        print("Starting stream...")
        args = {"follow": users, "language": "en"}

        while True:
            try:
                # start stream
                self.stream.statuses.filter(**args)

            except:
                # catch exceptions and restart
                self.stop()
                print("Restarting stream...")
                sleep(5) # wait
                continue

            else:
                # end if requested
                print("Breaking...")
                break

    def stop(self):
        """Stop the twitter stream."""

        # end stream
        self.stream.disconnect()
        print("Ending stream...")

    def restart(self):
        """Restart the twitter stream."""

        self.stop()
        self.start()
