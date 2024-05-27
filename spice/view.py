from flask import (
    Blueprint,
    render_template,
    current_app,
    send_from_directory,
    abort,
    url_for,
    g,
)

from . import handlers
from . import database
from . import models

bp = Blueprint("view", __name__)


def can_view_file(record):
    if record.access == "private":
        return g.user
    return True


@bp.route("/<key>/<filename>")
def view_raw(key, filename):
    record = database.get_db().query(models.File).filter_by(key=key).first()

    if record is not None and can_view_file(record):
        return send_from_directory(current_app.config["UPLOAD_FOLDER"], record.filename)

    abort(404)

@bp.route("/cache/<key>/<filename>")
def view_cache(key, filename):
    record = database.get_db().query(models.File).filter_by(key=key).first()
    print('heey', record)

    handler = handlers.get_handler_instance(record)
    print('heey', handler.thumbnail_file)
    if record is not None and can_view_file(record):
        return send_from_directory(current_app.config["CACHE_FOLDER"], handler.thumbnail_file)

    abort(404)


@bp.route("/<key>")
def view(key):
    db = database.get_db()
    record = db.query(models.File).filter_by(key=key).first()

    if record is not None and can_view_file(record):
        record.views += 1
        db.add(record)
        db.commit()

        handler = handlers.get_handler_instance(record)
        return render_template(
            handler.template,
            current_user=g.user,
            current_path=url_for(".view", key=key),
            handler=handler,
        )

    abort(404)
