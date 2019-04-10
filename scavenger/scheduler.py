import atexit

from scavenger.sender import send_next_item
from apscheduler.schedulers.background import BackgroundScheduler


def schedule_rounds():
    print('Scheduling rounds.')
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=send_next_item, trigger="interval", seconds=5)
    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())