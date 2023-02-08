from apscheduler.schedulers.blocking import BlockingScheduler
from peeve_job import start as run_job
import requests

sched = BlockingScheduler()

# Runs daily at 7pm UTC
@sched.scheduled_job('cron', day_of_week='mon-sun', hour=19)
def tweet_job():
    run_job()

# Keep web instance awake by pinging every 25 minutes (1500 seconds)
@sched.scheduled_job('interval', day_of_week='mon-sun', seconds=1500)
def awake_job():
    r = requests.get('https://pet-peeve.herokuapp.com/')

sched.start()
