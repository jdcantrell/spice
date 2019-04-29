from flask import url_for


class DefaultHandler:
    type = 'default'
    extensions = []
    template = 'view.html'

    def __init__(self, record):
        self.record = record

    def process(self):
        pass

    def delete(self):
        pass

    @property
    def link(self):
        return url_for('view.view', key=self.record.key)

    @property
    def raw(self):
        return url_for('view.view_raw', key=self.record.key, filename=self.record.name)

    @property
    def data(self):
        return self.record
