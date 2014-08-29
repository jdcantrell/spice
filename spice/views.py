from flask import session, escape, redirect, request, url_for, render_template, send_from_directory
from flask.ext.login import login_user, logout_user, current_user, login_required

from werkzeug.security import check_password_hash
from werkzeug import secure_filename

from spice import app, login_manager
from spice.database import db_session
from spice.models import User, File
from spice.handlers import get_handler

import time
import uuid
import json
import os

@login_manager.user_loader
def load_user(user_id):
  return db_session.query(User).get(int(user_id))

def file_json(record):
  return json.dumps({
    'id': record.id,
    'name': record.name,
    'views': record.views,
    'access': record.access,
    'created': record.created.strftime('%Y-%m-%d'),
    'type': record.handler,
    'key': record.key
    })

@app.route('/')
def index():
  files = []
  if current_user.is_authenticated():
    files = db_session.query(File).order_by(File.id.desc()).all()
  else:
    files = db_session.query(File).filter_by(access='public').order_by(File.id.desc()).all()

  json = [file_json(r) for r in files]

  return render_template('list.html',
    current_user=current_user,
    files=files,
    json=json,
    static_web_path=app.config['STATIC_WEB_PATH'],
    upload_web_path=app.config['UPLOAD_WEB_PATH'],
  )

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form.get('username', None)
    pw = request.form.get('password', None)
    if username != None and pw != None:
      users = db_session.query(User).filter_by(username=username)

      for user in users:
        if check_password_hash(user.password, pw):
          login_user(user, remember=True)
          return redirect(url_for('index'))

    time.sleep(5)

  return render_template('login.html',
    static_web_path=app.config['STATIC_WEB_PATH'],
    upload_web_path=app.config['UPLOAD_WEB_PATH'],
  )

@app.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect(url_for('index'))

@app.route('/file/<id>', methods=['PUT'])
@login_required
def update(id):
  record = db_session.query(File).get(id)
  if record is not None:
    record.access = request.json['access']
    record.name = request.json['name']
    record.handler = request.json['type']
    record.key = request.json['key']
    db_session.add(record)
    db_session.commit()
    return '', 204
  return '', 404

@app.route('/file/<id>', methods=['DELETE'])
@login_required
def delete(id):
  record = db_session.query(File).get(id)
  if record is not None:
    db_session.delete(record)
    db_session.commit()
    return '', 204
  return '', 404

@app.route('/file', methods=['POST'])
@login_required
def create():
  file = request.files['file']
  if file:
    filename = secure_filename(file.filename)
    _, extension = os.path.splitext(filename)

    unique_name = "%s%s" % (str(uuid.uuid4()), extension)
    path = app.config['UPLOAD_FOLDER']

    while os.path.isfile(os.path.join(path, unique_name)):
      unique_name = "%s%s" % (str(uuid.uuid4()), extentsion)

    file.save(os.path.join(path, unique_name))

    access = request.form['access']
    record = File(filename, unique_name, path, get_handler(extension)['name'], extension, access, current_user.id)

    db_session.add(record)
    db_session.commit()

    return file_json(record)

def can_view_file(record):
  if record.access == 'private':
    return current_user.is_authenticated()
  return True

@app.route('/<key>/<filename>')
def view_raw(key, filename):
  #get record
  record = db_session.query(File).filter_by(key=key).first()

  if record is not None and can_view_file(record):
    return send_from_directory(record.path, record.filename)

  return 'herp derp'

@app.route('/<key>')
def view(key):
  #get record
  record = db_session.query(File).filter_by(key=key).first()

  if record is not None and can_view_file(record):
    record.views += 1
    db_session.add(record)
    db_session.commit()

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

  return 'herp derp'
