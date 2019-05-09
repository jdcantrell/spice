import json

from flask_login import current_user

from spice.database import get_db
from spice.models import File
from spice.handlers import get_handler_instance


def file_json(record):
    return json.dumps(
        {
            "id": record.id,
            "name": record.name,
            "views": record.views,
            "access": record.access,
            "created": record.created.strftime("%Y-%m-%d"),
            "type": record.handler,
            "key": record.key,
        }
    )


def get_file_data(limit=50, offset=0):
    files = []
    db = get_db()
    if current_user.is_authenticated:
        query = db.query(File)
    else:
        query = db.query(File).filter_by(access="public")

    files = query.order_by(File.id.desc()).limit(limit).offset(offset).all()

    json = []
    handlers = []
    for record in files:
        json.append(file_json(record))
        handlers.append(get_handler_instance(record))

    return (json, handlers)
