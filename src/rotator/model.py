from flask import render_template, Blueprint
from rotator.auth import requires_auth

blueprint = Blueprint('model', 'model')


@blueprint.route('/')
@requires_auth
def landing():
    return render_template('index.html')
