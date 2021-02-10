from apscheduler.schedulers.blocking import BlockingScheduler
from peeve_job import start as run_job

sched = BlockingScheduler()

# Runs daily at 5pm UTC
@sched.scheduled_job('cron', day_of_week='mon-sun', hour=17)
def scheduled_job():
    run_job()

sched.start()