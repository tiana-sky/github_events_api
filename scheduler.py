import schedule
import time
from main import update_github_events

schedule.every(1).hours.do(update_github_events)

while True:
    schedule.run_pending()
    time.sleep(1)