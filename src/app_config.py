import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

SECRET_KEY = '_JurekOwsiak#1994'
DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'rotator.db')
DATABASE_CONNECT_OPTIONS = {}

del os
