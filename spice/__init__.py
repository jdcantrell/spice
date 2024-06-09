from flask import Flask
import os


class DefaultConfig(object):
    UPLOAD_FOLDER = os.path.abspath("./uploads")
    DATABASE_FILE = os.path.abspath("./spice.sql")
    CACHE_FOLDER = os.path.abspath("./cache")


app = Flask(__name__)

app.config.from_object(DefaultConfig)
app.config.from_envvar("SPICE_SETTINGS", silent=True)

if app.config["SECRET_KEY"] is None:
    print("No secret key set, have you set and exported SPICE_SETTINGS?")

print(f"Using db file {app.config["DATABASE_FILE"]}")


from . import database

database.init_app(app)

from . import auth

app.register_blueprint(auth.bp)

from . import files

app.register_blueprint(files.bp)
app.add_url_rule("/<key>/<filename>", endpoint="files.view_raw")
app.add_url_rule("/<key>", endpoint="files.view")

from . import view

app.register_blueprint(view.bp)
app.add_url_rule("/cache/<key>/<filename>", endpoint="view.view_cache")

from . import table

app.register_blueprint(table.bp)
app.add_url_rule("/", endpoint="table.index")

from . import log

app.register_blueprint(log.bp)

from . import tiles

app.register_blueprint(tiles.bp)


@app.cli.command()
def process():
    from spice.models import File
    from spice.database import get_db
    from spice.handlers import get_handler_instance

    db_session = get_db()
    files = db_session.query(File).order_by(File.id.desc()).all()

    for record in files:
        handler = get_handler_instance(record)
        handler.process()
        db_session.add(handler.record)

        db_session.commit()


@app.cli.command()
def create_user():
    from spice.models import User
    from spice.database import get_db

    db_session = get_db()
    name = input("User name: ")
    password = input("Password: ")

    user = User(name, password)

    db_session.add(user)
    db_session.commit()

    print("User created: %r" % user.id)


@app.cli.command()
def init_db():
    from spice.database import init_db

    init_db()

    print("Database initialized")
