from datetime import datetime, timedelta
from time import tzname

from pytz import utc

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from password_generator.email.email_service.gmail_service import send_mail

__jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///../generator.db')
}
__executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}
__job_defaults = {
    'coalesce': False,
    'max_instances': 3
}
__scheduler = BackgroundScheduler(jobstores=__jobstores, executors=__executors, job_defaults=__job_defaults, timezone=utc)


def init_scheduler():
    __scheduler.start()


def schedule_test(email: str, uuid: str):
    current_time = datetime.now()
    if not __scheduler.running:
        init_scheduler()

    __scheduler.add_job(send_mail, 'date', run_date=current_time + timedelta(seconds=1),
                        timezone=tzname[0], args=[email, uuid, 1])
    __scheduler.add_job(send_mail, 'date', run_date=current_time + timedelta(seconds=3),
                        timezone=tzname[0], args=[email, uuid, 3])
    __scheduler.add_job(send_mail, 'date', run_date=current_time + timedelta(seconds=7),
                        timezone=tzname[0], args=[email, uuid, 7])