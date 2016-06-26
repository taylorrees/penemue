import time
from twython import Twython
from credentials import app_key, app_secret, auth_token, auth_secret


def notify(reset):
    s = reset - time.time()
    print("Limiting...")
    print("Next request: %d mins %02d secs" % divmod(s, 60))


def limiter(request):
    def decorator(f):
        def wrapper(*args):
            """
            A small decorator function to provide Twitter API rate
            limiting. A request is made to the API to get the number
            of remaining requests. If no requests remain then the
            current thread must wait until the specified reset time.

            E.g.

            @limiter("users/lookup")
            def lookup_user():
                something()

            """

            twitter = Twython(app_key, app_secret, auth_token, auth_secret)
            resource = request.split("/")[0]

            # rate_limit_status has rate limit
            a = twitter.get_application_rate_limit_status()
            b = a["resources"]["application"]["/application/rate_limit_status"]
            c = a["resources"][resource]["/%s" % request]

            now = time.time()

            # respect rate_limit_status limits
            if b["remaining"] == 0:
                # wait for reset
                reset = b["reset"]
                notify(reset)
                time.sleep(reset - now)

            # respect requested limits
            if c["remaining"] == 0:
                # wait for reset
                reset = c["reset"]
                notify(reset)
                time.sleep(reset - now)

            return f(*args)
        return wrapper
    return decorator
