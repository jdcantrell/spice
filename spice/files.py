import uuid
import os

from flask import (
    Blueprint,
    request,
    current_app,
    send_from_directory,
    abort,
    url_for,
    render_template,
)

from flask_login import current_user, login_required

from werkzeug import secure_filename

from .database import get_db
from .models import File
from .handlers import get_handler, get_handler_instance
from .util import file_json

bp = Blueprint("files", __name__, url_prefix="/file")


@bp.route("/<id>", methods=["PUT"])
@login_required
def update(id):
    record = get_db().query(File).get(id)
    if record is not None:
        record.access = request.json["access"]
        record.name = request.json["name"]
        record.handler = request.json["type"]
        record.key = request.json["key"]
        get_db().add(record)
        get_db().commit()
        return "", 204
    return "", 404


@bp.route("/<id>", methods=["DELETE"])
@login_required
def delete(id):
    record = get_db().query(File).get(id)
    if record is not None:
        handler = get_handler_instance(record)
        handler.delete()

        get_db().delete(record)
        get_db().commit()
        return "", 204
    return "", 404


@bp.route("/", methods=["POST"])
@login_required
def create():
    print("hello")
    file = request.files["file"]
    if file:
        filename = secure_filename(file.filename)
        _, extension = os.path.splitext(filename.lower())

        unique_name = "%s%s" % (str(uuid.uuid4()), extension)
        path = current_app.config["UPLOAD_FOLDER"]

        while os.path.isfile(os.path.join(path, unique_name)):
            unique_name = "%s%s" % (str(uuid.uuid4()), extension)

        file.save(os.path.join(path, unique_name))

        handler_class = get_handler(extension)
        data = File(
            filename,
            unique_name,
            path,
            handler_class.type,
            extension,
            request.form["access"],
            current_user.id,
        )

        handler = handler_class(
            data,
            current_app.config["CACHE_FOLDER"],
            current_app.config["UPLOAD_FOLDER"],
        )
        handler.process()

        get_db().add(handler.record)
        get_db().commit()

        return file_json(handler.record)
    return "No file", 400


def can_view_file(record):
    if record.access == "private":
        return current_user.is_authenticated
    return True


@bp.route("/<key>/<filename>")
def view_raw(key, filename):
    record = get_db().query(File).filter_by(key=key).first()

    if record is not None and can_view_file(record):
        return send_from_directory(current_app.config["UPLOAD_FOLDER"], record.filename)

    abort(404)


@bp.route("/<key>")
def view(key):
    db = get_db()
    record = db.query(File).filter_by(key=key).first()

    if record is not None and can_view_file(record):
        record.views += 1
        db.add(record)
        db.commit()

        handler = get_handler_instance(record)
        return render_template(
            handler.template, current_path=url_for(".view", key=key), handler=handler
        )

    abort(404)
