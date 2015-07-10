import db_back
from flask import Flask

from rotator.keys import SCHED_HOUR, SCHED_MINUTE, SCHED_JOBID
from rotator.schedule import scheduler
from rotatordb import db_session

app = Flask(__name__)
app.config.from_object('app_config')

from rotator import db_config

app.config.update(db_config.load_config())

scheduler.add_job(db_back.create_backup(), 'cron', hour=app.config[SCHED_HOUR],
                  minute=app.config[SCHED_MINUTE], id=app.config[SCHED_JOBID])
scheduler.start()

from rotator import model_blueprint

app.register_blueprint(model_blueprint.blueprint)


@app.teardown_request
def remove_db_session(exception):
    db_session.remove()
