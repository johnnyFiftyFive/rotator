from flask import render_template, Blueprint
from database import RotatorDB
from rotator.auth import requires_auth

blueprint = Blueprint('model', 'model')


@blueprint.route('/')
@requires_auth
def landing():
    db_session = RotatorDB().get_session()
    return render_template('index.html')
