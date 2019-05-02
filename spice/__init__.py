from flask import Flask
from flask_login import LoginManager


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_pyfile("../settings.cfg", silent=False)
    else:
        app.config.from_mapping(test_config)

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

    from . import view

    app.register_blueprint(view.bp)

    from . import table

    app.register_blueprint(table.bp)
    app.add_url_rule("/", endpoint="table.index")

    from . import log

    app.register_blueprint(log.bp)

    from . import tiles

    app.register_blueprint(tiles.bp)

    return app
