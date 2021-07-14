from datetime import date, datetime
from os import environ
from time import sleep

from twitter_api import oauth_login, post_tweet, get_latest_tweets, retweet

def start():
    print("Starting up...")
    api = oauth_login()
    SLEEP_INTERVAL = 60 * 20
    USER_ID = int(environ.get("USER_ID"))
    USERNAME = environ.get("USERNAME")
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
            post_tweet(api, f"happy birthday {USERNAME}! hope you have a good one. love you!")
        elif (date.today().month == 12) and (date.today().day == 25):
            post_tweet(api, "merry christmas! hope Eve has a good one.")
        elif tweet_day >= TWEET_INTERVAL:
            f = open("tweets.txt")
            content = f.readlines()
            if line >= len(content):
                line = 0
            tweet = content[line].replace("???", USERNAME)
            post_tweet(api, tweet)
            f.close()
            tweet_day = 0
        elif retweet_day >= RETWEET_INTERVAL:
            latest_tweets = get_latest_tweets(api, USER_ID)
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
        for i in range(3 * 24):
            print("Sleeping...")
            sleep(SLEEP_INTERVAL)


if __name__ == "__main__":
    start()