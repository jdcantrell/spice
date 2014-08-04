from flask import session, escape, redirect, request, url_for
from spice import app

from werkzeug.security import check_password_hash
from spice.database import db_session
from spice.models import User
from spice.handlers import get_handler

import time
import uuid
import json

@app.route('/')
def index():
  if 'user' in session:
    return ' %s' % session['user']['name']
  return 'Hai'

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form.get('username', None)
    pw = request.form.get('password', None)
    if username != None and pw != None:
      users = db_session.query(User).filter_by(username=username)

      for user in users:
        if check_password_hash(user.password, pw):
          session['user'] = {
            'id': user.id,
            'name': user.username
          }
          break

    if 'user' not in session:
      pass
      time.sleep(5)
      return redirect(url_for('login'))
    else:
      return redirect(url_for('index'))

  return '''
    <form action="" method="post">
        <p><input type=text name=username>
        <p><input type=text name=password>
        <p><input type=submit value=Login>
    </form>
  '''

@app.route('/upload', methods=['POST'])
def upload():
  file = request.files['file']
  if file:
    filename = secure_filename(file.filename)
    unique_name = uuid.uuid4()
    path = app.config['UPLOAD_FOLDER']

    while os.path.isfile(os.path.join(path, unique_name)):
      unique_name = uuid.uuid4()

    file.save(os.path.join(path, unique_name))

    _, filetype = os.path.splitext(filename)

    record = File(filename, unique_path, path, get_handler(filetype), filetype, user)

    db_session.add(user)
    db_session.commit()

    return json.dumps({
      'id': record.id,
      'name': record.name,
      'views': record.views,
      'created': record.created,
      'url': '/%' % record.get_key()
     })

@app.route('/<key>')
def view(key):
  #get record
  record = db_session.query(File).filter_by(id=key)
  if record is None:
    record = db_session.query(File).filter_by(key=key)


  if record is not None:
    return '%/%' % (record.path, record.filename)

  return 'oops not found'


