from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from reserveChecker import reservejob


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(reservejob.reservation_expire, "interval", seconds=60)
    scheduler.start()
