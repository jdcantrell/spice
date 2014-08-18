from flask import Flask
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config.from_pyfile('../settings.cfg', silent=True)

login_manager = LoginManager()
login_manager.init_app(app)

from spice.database import db_session
import spice.views

@app.teardown_appcontext
def shutdown_session(exception=None):
  db_session.remove()
