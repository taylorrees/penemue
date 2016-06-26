import sys
import monitor
import time
from threading import Thread, Timer

if __name__ == "__main__":

    tweets = monitor.Monitor()
    users = monitor.Users()
    seconds = lambda hours : hours * 60 * 60
    U = seconds(hours=6) # update users every (seconds)
    R = seconds(hours=120) # restart stream every (seconds)

    # start stream
    Thread(target=tweets.start).start()

    update = time.time() + U
    restart = time.time() + R

    while True:

        if update - time.time() <= 0:
            # update users
            update = time.time() + U
            Thread(target=users.update).start()

        if restart - time.time() <= 0:
            # restart stream
            restart = time.time() + R
            Thread(target=tweets.restart).start()
