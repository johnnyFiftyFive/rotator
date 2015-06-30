from db_back import create_backup
import db_back
from flask import render_template, Blueprint
from rotator import db_log
from rotator.auth import requires_auth
from rotator.db_log import error
from scratchrotator import check_db_config

blueprint = Blueprint('model', 'model')


@blueprint.route('/')
@requires_auth
def landing():
    lacking_keys = check_db_config()
    if not lacking_keys:
        create_backup()
    if lacking_keys:
        error('Braki w konfiguracji', dict(lacking_keys=lacking_keys))
    return render_template('index.html', lacking_keys=lacking_keys)


@blueprint.route('/do_backup')
def do_backup():
    connection = db_back.get_connection()
    if not connection or not connection.is_connected():
        db_log.error('Brak polaczenia z baza.', dict(connection_info=str(connection)))
        return render_template('index.html', back_status=99)
    return render_template('index.html', back_status=create_backup())
