from flask import Flask


class DefaultConfig(object):
    UPLOAD_FOLDER = "./uploads"
    DATABASE_FILE = "./spice.sql"
    CACHE_FOLDER = "./cache"


app = Flask(__name__)

app.config.from_object(DefaultConfig)
app.config.from_envvar("SPICE_SETTINGS", silent=True)

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

from . import table

app.register_blueprint(table.bp)
app.add_url_rule("/", endpoint="table.index")

from . import log

app.register_blueprint(log.bp)

from . import tiles

app.register_blueprint(tiles.bp)
