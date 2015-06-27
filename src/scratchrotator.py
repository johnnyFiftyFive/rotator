# coding=utf-8
from database import db_session

from flask import Flask
import os
from os.path import getmtime
from rotator import model

app = Flask(__name__)
app.config.from_object('app_config')

app.register_blueprint(model.blueprint)


@app.teardown_request
def remove_db_session(exception):
    db_session.remove()


if __name__ == '__main__':
    app.run(debug=True)


def remove_oldest(directory, count):
    """
    Deletes the oldest files from given directory

    :param directory: directory to prune
    :param count: number of files, which will survive
    """
    files = os.listdir(directory)
    if len(files) < count:
        return
    files.sort(key=lambda f: getmtime(f))
    for f in files[:count]:
        os.remove(f)
