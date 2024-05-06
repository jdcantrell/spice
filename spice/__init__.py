import click
from flask import Flask
from flask_login import LoginManager

class DefaultConfig(object):
    UPLOAD_FOLDER = './uploads'
    DATABASE_FILE = './spice.sql'
    CACHE_FOLDER = './cache'

app = Flask(__name__)

app.config.from_object(DefaultConfig)
app.config.from_envvar("SPICE_SETTINGS", silent=True)

login_manager = LoginManager()
login_manager.init_app(app)

from . import database

database.init_app(app)

from . import models

@login_manager.user_loader
def load_user(user_id):
    return database.get_db().query(models.User).get(int(user_id))

from . import auth

app.register_blueprint(auth.bp)

from . import files

app.register_blueprint(files.bp)
app.add_url_rule("/<key>/<filename>", endpoint="files.view_raw")
app.add_url_rule("/<key>", endpoint="files.view")

from . import view

app.register_blueprint(view.bp)

from . import table

app.register_blueprint(table.bp)
app.add_url_rule("/", endpoint="table.index")

from . import log

app.register_blueprint(log.bp)

from . import tiles

app.register_blueprint(tiles.bp)


@click.group()
def cli():
    pass


@cli.command()
@click.option("--name", prompt="Enter username")
@click.option(
    "--password", prompt="Enter password", hide_input=True, confirmation_prompt=True
)
def user_add(name, password):
    from spice.models import User
    from spice.database import db_session

    user = User(name, password)

    db_session.add(user)
    db_session.commit()

    print('User created: %r' % user.id)


@cli.command()
def create_db():
    from spice import app
    from spice.database import init_db
    init_db()

    print("Database init")

@cli.command()
def process():
    from spice.models import File
    from spice.database import db_session
    from spice.handlers import get_handler_instance
    files = db_session.query(File).order_by(File.id.desc()).all()

    for record in files:
        handler = get_handler_instance(record)
        handler.process()
        db_session.add(handler.record)

        db_session.commit()
