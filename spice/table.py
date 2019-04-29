from flask import (
    Blueprint,  render_template, current_app
)

from flask_login import current_user

from . import util

bp = Blueprint('table', __name__, url_prefix='/table' )

@bp.route('/')
@bp.route('/<int:page>')
def index(page=0):
    page_size = 50
    json, files = util.get_file_data(page_size, page * page_size)

    next_page = False
    if (len(files) == page_size):
        next_page = page + 1

    return render_template(
        'table.html',
        current_user=current_user,
        files=files,
        json=json,
        prev_page=page - 1,
        next_page=next_page,
        static_web_path=current_app.config['STATIC_WEB_PATH'],
        upload_web_path=current_app.config['UPLOAD_WEB_PATH'],
        root_web_path=current_app.config['ROOT_WEB_PATH'],
    )

