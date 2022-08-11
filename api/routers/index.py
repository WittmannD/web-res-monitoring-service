import os

from flask import Blueprint, send_from_directory, current_app

blueprint = Blueprint('index', __name__)


@blueprint.route('/', defaults={'path': ''})
@blueprint.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(current_app.static_folder + '/' + path):
        return send_from_directory(current_app.static_folder, path)
    else:
        return send_from_directory(current_app.static_folder, 'index.html')
