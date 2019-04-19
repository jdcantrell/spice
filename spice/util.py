from flask_login import current_user

from spice.database import db_session
from spice.models import File
from spice.handlers import  get_handler_instance

def get_file_data(limit=50, offset=0):
    files = []
    if current_user.is_authenticated:
        query = db_session.query(File)
    else:
        query = db_session.query(File).filter_by(access='public')

    files = query.order_by(File.id.desc()).limit(limit).offset(offset).all()

    json = []
    handlers = []
    for record in files:
        json.append(file_json(record))
        handlers.append(get_handler_instance(record))

    return (json, handlers)
