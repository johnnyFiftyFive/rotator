import os
from builtins import print
from time import ctime
from os.path import getmtime

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



