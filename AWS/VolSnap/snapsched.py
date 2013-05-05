from datetime import datetime
from time import sleep
from apscheduler.scheduler import Scheduler

# Start the scheduler
sched = Scheduler(standalone=True)
    
# Define the function that is to be executed
@sched.cron_schedule(second="*/10")
def my_job():
    print 'text'

print sched.get_jobs()
sched.start()
sched.shutdown()