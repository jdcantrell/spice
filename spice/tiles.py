from flask import Blueprint, render_template

from flask_login import current_user

from . import util

bp = Blueprint("tiles", __name__, url_prefix="/tiles")


@bp.route("/")
@bp.route("/<int:page>")
def tile(page=0):
    page_size = 50
    json, files = util.get_file_data(page_size, page * page_size)

    next_page = False
    if len(files) == page_size:
        next_page = page + 1

    return render_template(
        "tiles.html",
        current_user=current_user,
        files=files,
        json=json,
        prev_page=page - 1,
        next_page=next_page,
    )
