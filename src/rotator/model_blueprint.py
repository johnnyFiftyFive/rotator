import json

from db_back import create_backup
import db_back
from flask import render_template, Blueprint, url_for, flash
from rotator.auth import requires_auth
from rotator.db_log import error
from rotator.keys import BACK_DB_CONFIG_KEYS
from rotatordb import db_session, Backup
from starter import app
from werkzeug.utils import redirect

blueprint = Blueprint('model', 'model')


def gather_backups():
    return db_session.query(Backup).filter(Backup.status != 255).order_by(Backup.created.desc()).all();


@blueprint.route('/')
@requires_auth
def landing():
    lacking_keys = check_db_config()
    if lacking_keys:
        error('Braki w konfiguracji', dict(lacking_keys=lacking_keys))
    entries = gather_backups()
    return render_template('index.html', lacking_keys=lacking_keys, entries=entries)


@blueprint.route('/do_backup')
@requires_auth
def do_backup():
    back_status = create_backup()
    flash(back_status, category='status')
    return redirect(url_for('model.landing'))


@blueprint.route('/delete/<int:back_id>', methods=['POST'])
@requires_auth
def delete(back_id):
    resp = db_back.delete(back_id)
    return json.dumps(resp)


def check_db_config():
    lacking = []
    for k in BACK_DB_CONFIG_KEYS:
        if not app.config.get(k):
            lacking.append(k)
    return lacking
