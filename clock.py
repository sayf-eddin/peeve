from apscheduler.schedulers.blocking import BlockingScheduler
from peeve_job import start as run_job

sched = BlockingScheduler()

# Runs daily at 7pm UTC
@sched.scheduled_job('cron', day_of_week='mon-sun', hour=19)
def scheduled_job():
    run_job()

sched.start()
