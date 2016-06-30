from sys import exit
from time import time
from collect import Collect
from monitor import MonitorTweets
from monitor import MonitorUsers
from threading import Thread
from threading import Timer
from json import load

if __name__ == "__main__":

    try:

        # hours to seconds
        seconds = lambda hours: hours * 60 * 60

        mt = MonitorTweets()
        mu = MonitorUsers()
        U = seconds(hours=6)   # update users every (seconds)
        R = seconds(hours=24)  # restart stream every (seconds)

        # get journalists from twitter lists
        journalists = load(open("journalists.json"))
        collect = Collect(lists=journalists)
        collect.store()

        # get news organisations from twitter lists
        organisations = load(open("organisations.json"))
        collect = Collect(lists=organisations, refine=False, append=True)
        collect.store()

        # start stream
        Thread(target=mt.start).start()

        update = time() + U
        restart = time() + R

        while True:

            if update - time() <= 0:
                # update users
                update = time() + U
                Thread(target=mu.update).start()

            if restart - time() <= 0:
                # restart stream
                restart = time() + R
                Thread(target=mt.restart).start()

    except KeyboardInterrupt as e:
        # exit gracefully
        print()
        mt.stop()
        exit()
