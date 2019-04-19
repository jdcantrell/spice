from flask import Flask
from flask_login import LoginManager

def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_pyfile('../settings.cfg', silent=False)
    else:
        app.config.from_mapping(test_config)

    login_manager = LoginManager()
    login_manager.init_app(app)

    from spice.database import db_session
    db.init_app(app)

    import spice.views

    from . import log
    app.register_blueprint(log.bp)
