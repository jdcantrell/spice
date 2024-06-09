from flask import Blueprint, render_template
from flask import g


from . import util

bp = Blueprint("table", __name__, url_prefix="/table")


@bp.route("/")
@bp.route("/<int:page>")
def index(page=0):
    page_size = 50
    json, files = util.get_file_data(page_size, page * page_size)

    next_page = False
    if len(files) == page_size:
        next_page = page + 1

    return render_template(
        "table.html",
        current_user=g.user,
        files=files,
        json=json,
        view="table.index",
        prev_page=page - 1,
        next_page=next_page,
    )
