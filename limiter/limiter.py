from credentials import app_key
from credentials import app_secret
from credentials import auth_token
from credentials import auth_secret
from twython import Twython
from time import time
from time import sleep


def notify(reset):
    secs = reset - time()
    print("Limiting...")
    print("Next request:")
    print("%d mins %02d secs" % divmod(secs, 60))


def limiter(request):
    def decorator(f):
        def wrapper(*args, **kwargs):
            """
            A small decorator function to provide Twitter API rate
            limiting. A request is made to the API to get the number
            of remaining requests. If no requests remain then the
            current thread must wait until the specified reset time.

            See: https://dev.twitter.com/rest/public/rate-limits

            E.g.

            @limiter("users/lookup")
            def lookup_user():
                something()

            """

            cr = [app_key, app_secret, auth_token, auth_secret]
            twitter = Twython(*cr)
            resource = request.split("/")[0]

            # rate_limit_status has rate limit
            a = twitter.get_application_rate_limit_status()

            b = a["resources"]
            b = b["application"]
            b = b["/application/rate_limit_status"]

            c = a["resources"]
            c = c[resource]
            c = c["/%s" % request]

            now = time()

            # respect rate_limit_status limits
            if b["remaining"] == 0:
                # wait for reset
                reset = b["reset"]
                notify(reset)
                sleep(reset - now)

            # respect requested limits
            if c["remaining"] == 0:
                # wait for reset
                reset = c["reset"]
                notify(reset)
                sleep(reset - now)

            return f(*args, **kwargs)
        return wrapper
    return decorator
