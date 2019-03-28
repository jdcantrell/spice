from spice import app
from flask import url_for


class DefaultHandler:
    type = 'default'
    extensions = []
    upload_path = app.config['UPLOAD_FOLDER']
    web_path = app.config['UPLOAD_WEB_PATH']
    cache_path = app.config['CACHE_FOLDER']
    cache_web_path = app.config['CACHE_WEB_PATH']
    root_web_path = app.config['ROOT_WEB_PATH']
    template = 'view.html'

    def __init__(self, record):
        self.record = record

    def process(self):
        pass

    def delete(self):
        pass

    @property
    def link(self):
        return url_for('view', key=self.record.key)

    @property
    def raw(self):
        return url_for('view_raw', key=self.record.key, filename=self.record.name)

    @property
    def data(self):
        return self.record
