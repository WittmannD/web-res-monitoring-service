import os

from flask import Blueprint, send_from_directory, current_app

blueprint = Blueprint('pages', __name__)


@blueprint.route('/', defaults={'path': ''}, strict_slashes=False)
@blueprint.route('/<path:path>', strict_slashes=False)
def index(path):
    if path != "" and os.path.exists(current_app.static_folder + '/' + path):
        return send_from_directory(current_app.static_folder, path)
    else:
        return send_from_directory(current_app.static_folder, 'index.html')
