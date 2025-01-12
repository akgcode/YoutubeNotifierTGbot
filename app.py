import schedule
import time
from try1 import job

schedule.every(60).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(3600)

# job()