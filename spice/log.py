from flask import Blueprint, render_template, g

from . import util
from .database import get_db
from .models import File

bp = Blueprint("log", __name__, url_prefix="/log")


def can_view_file(record):
    if record.access == "private":
        return g.user
    return True


@bp.route("/")
@bp.route("/<int:page>")
def log(page=0):
    page_size = 30
    json, files = util.get_file_data(page_size, page * page_size)

    next_page = False
    if len(files) == page_size:
        next_page = page + 1

    print(files)

    return render_template(
        "log.html",
        current_user=g.user,
        files=files,
        json=json,
        view="log.log",
        prev_page=page - 1,
        next_page=next_page,
    )


@bp.route("/html/<string:key>")
def get_item_html(key):
    record = get_db().query(File).filter_by(key=key).first()
    if can_view_file(record):
        handler = util.get_handler_instance(record)
        return render_template("log_item.html", current_user=g.user, file=handler)
