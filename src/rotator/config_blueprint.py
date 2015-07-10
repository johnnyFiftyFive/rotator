from flask import Blueprint
from rotator.auth import requires_auth

blueprint = Blueprint('config_model', 'config_model')


@blueprint.route('/settings/get', methods=['POST'])
@requires_auth
def get_settings():
    pass

@blueprint.route('/settings/update', methods=['PUT'])
@requires_auth
def get_settings():
    pass