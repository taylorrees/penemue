from twython import TwythonStreamer
from pprint import pprint


class Stream(TwythonStreamer):

    def on_success(self, data):
        # extend when in use
        # add required functions
        print(data)

    def on_error(self, status_code, data):
        print(status_code)

    def end(self):
        self.disconnect()
