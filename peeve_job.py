from datetime import date, datetime
from math import floor
from os import environ
from time import sleep

from twitter_api import oauth_login, post_tweet, get_latest_tweets, retweet

def start():
    print("Starting up...")
    api = oauth_login()
    USER_ID = int(environ.get("USER_ID"))
    USERNAME = environ.get("USERNAME")
    starting_day = environ.get("STARTING_DAY")
    starting_date = datetime.strptime(starting_day, "%B %d, %Y")
    today = datetime.today()
    days_since = (today - starting_date).days
    TWEET_INTERVAL = 6
    RETWEET_INTERVAL = 11
    tweet_day = days_since % TWEET_INTERVAL
    retweet_day = days_since % RETWEET_INTERVAL
    line = floor(days_since / TWEET_INTERVAL) - 1

    if (date.today().month == 1) and (date.today().day == 31):
        post_tweet(api, f"happy birthday {USERNAME}! hope you have a good one. love you!")
    elif (date.today().month == 12) and (date.today().day == 25):
        post_tweet(api, "merry christmas! hope Eve has a good one.")
    elif tweet_day == 0:
        f = open("tweets.txt")
        content = f.readlines()
        while line >= len(content):
            line = len(content) - line
            tweet = content[line].replace("???", USERNAME)
        post_tweet(api, tweet)
        f.close()
    elif retweet_day == 0:
        latest_tweets = get_latest_tweets(api, USER_ID)
        if latest_tweets:
            for latest_tweet in latest_tweets:
                created_date = datetime.strptime(latest_tweets[0]["created_at"].replace("+0000 ", ""), "%c")
                if RETWEET_INTERVAL <= ((today - created_date).days + 1):
                    break
                if latest_tweet["favorite_count"] >= 10:
                    retweet(api, latest_tweet["id"])
                    break

    print(f"Days since last tweet: {tweet_day}")
    print(f"Last tweet on line {line}")
    print(f"Days since last retweet: {retweet_day}")


if __name__ == "__main__":
    start()