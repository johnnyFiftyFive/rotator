import app_config
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.background import BackgroundScheduler
from rotator.schedule.listeners import execution_listener, error_listener

scheduler = BackgroundScheduler()
scheduler.add_listener(execution_listener, EVENT_JOB_EXECUTED)
scheduler.add_listener(error_listener, EVENT_JOB_ERROR)
