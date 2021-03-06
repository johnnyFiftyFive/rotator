from flask import Blueprint
from rotator.auth import requires_auth

blueprint = Blueprint('config_model', 'config_model')


@blueprint.route('/settings', methods=['POST'])
@requires_auth
def get_settings():
    pass


@blueprint.route('/settings', methods=['PUT'])
@requires_auth
def get_settings():
    pass