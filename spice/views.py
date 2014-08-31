from flask import session, escape, redirect, request, url_for, render_template, send_from_directory
from flask.ext.login import login_user, logout_user, current_user, login_required

from werkzeug.security import check_password_hash
from werkzeug import secure_filename

from spice import app, login_manager
from spice.database import db_session
from spice.models import User, File
from spice.handlers import get_handler, get_handler_instance

import time
import uuid
import json
import os
import inspect

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

  json = []
  handlers = []
  for record in files:
    json.append(file_json(record))
    handlers.append(get_handler_instance(record))

  return render_template('list.html',
    current_user=current_user,
    files=handlers,
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
    handler = get_handler_instance(record)
    handler.delete()

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
    _, extension = os.path.splitext(filename.lower())

    unique_name = "%s%s" % (str(uuid.uuid4()), extension)
    path = app.config['UPLOAD_FOLDER']

    while os.path.isfile(os.path.join(path, unique_name)):
      unique_name = "%s%s" % (str(uuid.uuid4()), extentsion)

    file.save(os.path.join(path, unique_name))

    handler_class = get_handler(extension)
    record = File(filename, unique_name, path, handler_class.type, extension, request.form['access'], current_user.id)

    #do any needed processing
    handler = handler_class(record)
    handler.process()

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

    handler = get_handler_instance(record)
    return render_template(
      handler.template,
      static_web_path=app.config['STATIC_WEB_PATH'],
      upload_web_path=app.config['UPLOAD_WEB_PATH'],
      handler=handler,
    )

  return 'herp derp'
