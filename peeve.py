from datetime import date, datetime
from http.client import BadStatusLine
from os import environ
from time import sleep
from urllib.error import URLError
import sys
import twitter

def oauth_login():
    CONSUMER_KEY = environ.get("CONSUMER_KEY")
    CONSUMER_SECRET = environ.get("CONSUMER_SECRET")
    ACCESS_TOKEN = environ.get("ACCESS_TOKEN")
    ACCESS_SECRET = environ.get("ACCESS_SECRET")

    auth = twitter.oauth.OAuth(ACCESS_TOKEN, ACCESS_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)

    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api

# Taken from https://github.com/mikhailklassen/Mining-the-Social-Web-3rd-Edition/
def make_twitter_request(twitter_api_func, max_errors=10, *args, **kw): 
    
    # A nested helper function that handles common HTTPErrors. Return an updated
    # value for wait_period if the problem is a 500 level error. Block until the
    # rate limit is reset if it's a rate limiting issue (429 error). Returns None
    # for 401 and 404 errors, which requires special handling by the caller.
    def handle_twitter_http_error(e, wait_period=2, sleep_when_rate_limited=True):
    
        if wait_period > 3600: # Seconds
            print('Too many retries. Quitting.', file=sys.stderr)
            raise e
    
        # See https://developer.twitter.com/en/docs/basics/response-codes
        # for common codes
    
        if e.e.code == 401:
            print('Encountered 401 Error (Not Authorized)', file=sys.stderr)
            return None
        elif e.e.code == 404:
            print('Encountered 404 Error (Not Found)', file=sys.stderr)
            return None
        elif e.e.code == 429: 
            print('Encountered 429 Error (Rate Limit Exceeded)', file=sys.stderr)
            if sleep_when_rate_limited:
                print("Retrying in 15 minutes...ZzZ...", file=sys.stderr)
                sys.stderr.flush()
                sleep(60*15 + 5)
                print('...ZzZ...Awake now and trying again.', file=sys.stderr)
                return 2
            else:
                raise e # Caller must handle the rate limiting issue
        elif e.e.code in (500, 502, 503, 504):
            print('Encountered {0} Error. Retrying in {1} seconds'\
                  .format(e.e.code, wait_period), file=sys.stderr)
            sleep(wait_period)
            wait_period *= 1.5
            return wait_period
        else:
            raise e

    # End of nested helper function
    
    wait_period = 2 
    error_count = 0 

    while True:
        try:
            return twitter_api_func(*args, **kw)
        except twitter.api.TwitterHTTPError as e:
            error_count = 0 
            wait_period = handle_twitter_http_error(e, wait_period)
            if wait_period is None:
                return
        except URLError as e:
            error_count += 1
            sleep(wait_period)
            wait_period *= 1.5
            print("URLError encountered. Continuing.", file=sys.stderr)
            if error_count > max_errors:
                print("Too many consecutive errors...bailing out.", file=sys.stderr)
                raise
        except BadStatusLine as e:
            error_count += 1
            sleep(wait_period)
            wait_period *= 1.5
            print("BadStatusLine encountered. Continuing.", file=sys.stderr)
            if error_count > max_errors:
                print("Too many consecutive errors...bailing out.", file=sys.stderr)
                raise

def post_tweet(api, tweet):
    print("Posting tweet")
    make_twitter_request(api.statuses.update, status=tweet)

def get_latest_tweets(api, user_id):
    print("Retrieving latest tweets")
    return make_twitter_request(api.statuses.user_timeline, user_id=user_id, 
        count=10, exclude_replies=True, include_rts=False)

def retweet(api, tweet_id):
    print("Retweeting")
    make_twitter_request(api.statuses.retweet, id=tweet_id)

def start():
    print("Starting up...")
    api = oauth_login()
    SLEEP_INTERVAL = 60 * 60
    CAITLIN_ID = 2172576189
    tweet_day = int(environ.get("TWEET_DAY"))
    retweet_day = int(environ.get("RETWEET_DAY"))
    TWEET_INTERVAL = 6
    RETWEET_INTERVAL = 11
    line = int(environ.get("TWEET_LINE"))
    last_retweet_id = 0

    while (datetime.today().hour - 5) != 12:
        print("Waiting for noon...")
        sleep(SLEEP_INTERVAL)

    while True:
        print("Waking up")
        if (date.today().month == 1) and (date.today().day == 31):
            post_tweet(api, "happy birthday @caitsands! hope you have a good one. love you!")
        elif (date.today().month == 12) and (date.today().day == 25):
            post_tweet(api, "merry christmas! hope Eve has a good one.")
        elif tweet_day >= TWEET_INTERVAL:
            f = open("tweets.txt")
            content = f.readlines()
            if line >= len(content):
                line = 0
            post_tweet(api, content[line])
            f.close()
            tweet_day = 0
        elif retweet_day >= RETWEET_INTERVAL:
            latest_tweets = get_latest_tweets(api, CAITLIN_ID)
            if latest_tweets:
                for latest_tweet in latest_tweets:
                    if latest_tweet["id"] == last_retweet_id:
                        break
                    if latest_tweet["favorite_count"] >= 10:
                        retweet(api, latest_tweet["id"])
                        last_retweet_id = latest_tweet["id"]
                        break
            retweet_day = 0

        print(f"Days since last tweet: {tweet_day}")
        print(f"Last tweet on line {line}")
        print(f"Days since last retweet: {retweet_day}")
        print(f"ID of last retweet: {last_retweet_id}")
    
        tweet_day += 1
        retweet_day += 1
        for i in range(24):
            print("Sleeping...")
            sleep(SLEEP_INTERVAL)


if __name__ == "__main__":
    start()