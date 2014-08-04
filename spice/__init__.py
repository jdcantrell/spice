from flask import Flask
app = Flask(__name__)

app.secret_key = 'haha'
app.config['UPLOAD_FOLDER'] = '/home/jcantrell/Projects/spice/uploads'
app.config['UPLOAD_WEB_PATH'] = '/uploads'

from spice.database import db_session
import spice.views

@app.teardown_appcontext
def shutdown_session(exception=None):
  db_session.remove()
