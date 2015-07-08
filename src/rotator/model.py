import json

import os
from db_back import create_backup
import db_back
from flask import render_template, Blueprint, url_for, flash
from rotator import db_log
from rotator.auth import requires_auth
from rotator.db_log import error
from rotatordb import db_session, Backup
from scratchrotator import check_db_config
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
    back = db_session.query(Backup).filter(Backup.id == back_id).first()
    back.status = 255
    resp = dict(status='ok')
    try:
        os.remove('backups/{}'.format(back.filename))
        db_log.info('Usunieto plik kopii', dict(file=back.filename))
    except Exception as err:
        resp['status'] = 'error'
        resp['filename'] = back.filename
        db_log.error('Nie mozna usunac pliku', dict(file=back.filename, error=err.message))
    if resp['status'] == 'ok':
        db_session.merge(back)
        db_session.commit()
    return json.dumps(resp)
