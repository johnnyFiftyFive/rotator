import json

from db_back import create_backup
from flask import render_template, Blueprint
from rotator.auth import requires_auth
from rotator.db_log import error
from scratchrotator import check_db_config

blueprint = Blueprint('model', 'model')


@blueprint.route('/')
@requires_auth
def landing():
    create_backup()
    lacking_keys = check_db_config()
    if lacking_keys:
        error('Braki w konfiguracji', dict(lacking_keys=lacking_keys))
    return render_template('index.html', lacking_keys=json.dumps(lacking_keys))
