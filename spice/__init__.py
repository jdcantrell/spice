from flask import Flask
app = Flask(__name__)
app.config.from_pyfile('../settings.cfg', silent=True)

from spice.database import db_session
import spice.views

@app.teardown_appcontext
def shutdown_session(exception=None):
  db_session.remove()
