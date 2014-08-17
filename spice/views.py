from flask import session, escape, redirect, request, url_for, render_template
from spice import app

from werkzeug.security import check_password_hash
from werkzeug import secure_filename
from spice.database import db_session
from spice.models import User, File
from spice.handlers import get_handler

import time
import uuid
import json
import os

@app.route('/')
def index():
  if 'user' in session:
    files = db_session.query(File).order_by(File.created.desc()).all()
    return render_template('list.html',
        files=files,
        static_web_path=app.config['STATIC_WEB_PATH'],
        upload_web_path=app.config['UPLOAD_WEB_PATH'],
      )
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

  return render_template('login.html',
        static_web_path=app.config['STATIC_WEB_PATH'],
        upload_web_path=app.config['UPLOAD_WEB_PATH'],
      )

@app.route('/upload', methods=['POST'])
def upload():
  file = request.files['file']
  if file:
    filename = secure_filename(file.filename)
    _, extension = os.path.splitext(filename)

    unique_name = "%s%s" % (str(uuid.uuid4()), extension)
    path = app.config['UPLOAD_FOLDER']

    while os.path.isfile(os.path.join(path, unique_name)):
      unique_name = "%s%s" % (str(uuid.uuid4()), extentsion)

    file.save(os.path.join(path, unique_name))


    print "type: %s(%s)" % (get_handler(extension), extension)
    record = File(filename, unique_name, path, get_handler(extension)['name'], extension, session['user']['id'])

    db_session.add(record)
    db_session.commit()

    return json.dumps({
      'id': record.id,
      'name': filename,
      'views': record.views,
      'created': record.created.strftime('%Y-%m-%d'),
      'type': record.handler,
      'key': record.get_key()
     })

@app.route('/u<key>')
def view(key):
  #get record
  record = db_session.query(File).get(key)

  if record is None:
    return 'herp derp'
  else:
    handler = get_handler(record.filetype)
    handler_class = handler['class']
    return render_template(
        handler['class'].template(),
        static_web_path=app.config['STATIC_WEB_PATH'],
        upload_web_path=app.config['UPLOAD_WEB_PATH'],
        record=record,
        handler=handler_class,
        data=handler_class.data(record)
    )

