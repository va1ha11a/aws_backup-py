from apscheduler.scheduler import Scheduler

# Start the scheduler
sched = Scheduler(standalone=True)
    
# Define the function that is to be executed
@sched.cron_schedule(second="*/10")
def my_job():
    print 'text'


sched.start()
sched.shutdown()