from apscheduler.schedulers.blocking import BlockingScheduler
from peeve_job import start as run_job
import requests

sched = BlockingScheduler()

# Keep web instance awake for a bit
@sched.scheduled_job('cron', day_of_week='mon-sun', hour=16, minute=50)
def awake_job():
    r = requests.get('https://pet-peeve.herokuapp.com/')

# Runs daily at 5pm UTC, 12pm EST
@sched.scheduled_job('cron', day_of_week='mon-sun', hour=17)
def tweet_job():
    run_job()

# Keep web instance awake by pinging every 25 minutes (1500 seconds)
# @sched.scheduled_job('interval', seconds=1500)
# def awake_job():
#     r = requests.get('https://pet-peeve.herokuapp.com/')

sched.start()
