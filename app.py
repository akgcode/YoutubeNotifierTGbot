import schedule
import time
from try1 import job

import subprocess

subprocess.run(["python", "database.py"])

schedule.every(60).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(3600)

# job()