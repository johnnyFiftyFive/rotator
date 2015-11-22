from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

from keys import SCHED_HOUR, SCHED_MINUTE, SCHED_JOBID
from schedule.listeners import execution_listener
from schedule.listeners import error_listener
from db_back import create_backup
import model_blueprint
import db_config

app = Flask(__name__)
app.config.from_object('app_config.config')

app.config.update(db_config.load_config())

scheduler = BackgroundScheduler()
scheduler.add_listener(execution_listener, EVENT_JOB_EXECUTED)
scheduler.add_listener(error_listener, EVENT_JOB_ERROR)
scheduler.add_job(create_backup, 'cron',
                  hour=int(app.config[SCHED_HOUR]),
                  minute=int(app.config[SCHED_MINUTE]),
                  id=app.config[SCHED_JOBID])
scheduler.start()

scheduler.get_jobs()
app.register_blueprint(model_blueprint.blueprint)

from rotatordb import db_session


@app.teardown_request
def remove_db_session(exception):
    db_session.remove()


if __name__ == '__main__':
    app.run(host='0.0.0.0')