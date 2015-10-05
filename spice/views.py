from flask import (
    redirect, request, url_for,
    render_template, send_from_directory, abort
)

from flask.ext.login import (
    login_user, logout_user, current_user, login_required
)

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


def get_file_data(limit=50, offset=0):
    files = []
    if current_user.is_authenticated:
        query = db_session.query(File)
    else:
        query = db_session.query(File).filter_by(access='public')

    files = query.order_by(File.id.desc()).limit(limit).offset(offset).all()

    json = []
    handlers = []
    for record in files:
        json.append(file_json(record))
        handlers.append(get_handler_instance(record))

    return (json, handlers)


@app.errorhandler(404)
def page_not_found(e):
    return render_template(
        '404.html',
        current_user=current_user,
        static_web_path=app.config['STATIC_WEB_PATH'],
        upload_web_path=app.config['UPLOAD_WEB_PATH'],
        root_web_path=app.config['ROOT_WEB_PATH'],
    ), 404


@app.route('/robots.txt')
def robots():
    return "User-agent: *\nDisallow: /"


@app.route('/')
@app.route('/<int:page>')
def index(page=0):
    page_size = 50
    json, files = get_file_data(page_size, page * page_size)

    next_page = False
    if (len(files) == page_size):
        next_page = page + 1

    return render_template(
        'list.html',
        current_user=current_user,
        files=files,
        json=json,
        prev_page=page - 1,
        next_page=next_page,
        static_web_path=app.config['STATIC_WEB_PATH'],
        upload_web_path=app.config['UPLOAD_WEB_PATH'],
        root_web_path=app.config['ROOT_WEB_PATH'],
    )


@app.route('/tiles')
@app.route('/tiles/<int:page>')
def tile(page=0):
    page_size = 50
    json, files = get_file_data(page_size, page * page_size)

    next_page = False
    if (len(files) == page_size):
        next_page = page + 1

    return render_template(
        'tiles.html',
        current_user=current_user,
        files=files,
        json=json,
        prev_page=page - 1,
        next_page=next_page,
        static_web_path=app.config['STATIC_WEB_PATH'],
        upload_web_path=app.config['UPLOAD_WEB_PATH'],
        root_web_path=app.config['ROOT_WEB_PATH'],
    )


@app.route('/login', methods=['GET'])
def login():
    return render_template(
        'login.html',
        static_web_path=app.config['STATIC_WEB_PATH'],
        upload_web_path=app.config['UPLOAD_WEB_PATH'],
        root_web_path=app.config['ROOT_WEB_PATH'],
    )


@app.route('/login', methods=['POST'])
def login_try():
    username = request.form.get('username', None)
    pw = request.form.get('password', None)
    if username is not None and pw is not None:
        users = db_session.query(User).filter_by(username=username)

        for user in users:
            if check_password_hash(user.password, pw):
                login_user(user, remember=True)
                return redirect(url_for('index'))

    time.sleep(5)

    return login()


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
            unique_name = "%s%s" % (str(uuid.uuid4()), extension)

        file.save(os.path.join(path, unique_name))

        handler_class = get_handler(extension)
        data = File(
            filename,
            unique_name,
            path,
            handler_class.type,
            extension,
            request.form['access'],
            current_user.id
        )

        handler = handler_class(data)
        handler.process()

        db_session.add(handler.record)
        db_session.commit()

        return file_json(handler.record)


def can_view_file(record):
    if record.access == 'private':
        return current_user.is_authenticated
    return True


@app.route('/<key>/<filename>')
def view_raw(key, filename):
    record = db_session.query(File).filter_by(key=key).first()

    if record is not None and can_view_file(record):
        return send_from_directory(record.path, record.filename)

    abort(404)


@app.route('/<key>')
def view(key):
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
            root_web_path=app.config['ROOT_WEB_PATH'],
            handler=handler,
        )

    abort(404)
