# coding=utf-8
import os
from os.path import getmtime
from rotator import app
from rotator.keys import BACK_DB_CONFIG_KEYS

if __name__ == '__main__':
    app.run()


def check_db_config():
    lacking = []
    for k in BACK_DB_CONFIG_KEYS:
        if not app.config.get(k):
            lacking.append(k)
    return lacking


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
