import json

import db_back
from flask import render_template, Blueprint, url_for, flash
from auth import requires_auth
from rotatordb import db_session, Backup
from werkzeug.utils import redirect

blueprint = Blueprint('model', 'model')


def gather_backups():
    return db_session.query(Backup).filter(Backup.status != 255).order_by(Backup.created.desc()).all();


@blueprint.route('/')
@requires_auth
def landing():
    entries = gather_backups()
    return render_template('index.html', entries=entries)


@blueprint.route('/do_backup')
@requires_auth
def do_backup():
    back_status = db_back.create_backup()
    flash(back_status, category='status')
    return redirect(url_for('model.landing'))


@blueprint.route('/delete/<int:back_id>', methods=['POST'])
@requires_auth
def delete(back_id):
    resp = db_back.delete(back_id)
    return json.dumps(resp)
