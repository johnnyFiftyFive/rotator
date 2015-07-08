from flask import Flask
from rotator.schedule import scheduler
from rotatordb import db_session

app = Flask(__name__)
app.config.from_object('app_config')

from rotator import db_config

app.config.update(db_config.load_config())
scheduler.start()

from rotator import model

app.register_blueprint(model.blueprint)


@app.teardown_request
def remove_db_session(exception):
    db_session.remove()
