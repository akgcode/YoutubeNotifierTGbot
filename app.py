import schedule
import time
from try1 import job

import subprocess

subprocess.run(["python", "database.py"])

schedule.every(60).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

# job()