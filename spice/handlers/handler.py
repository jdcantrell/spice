from flask import url_for, current_app


class DefaultHandler:
    type = "default"
    extensions = []
    template = "view.html"

    def __init__(self, record, cache_path, upload_path):
        self.record = record
        self.cache_path = cache_path
        self.upload_path = upload_path

    def process(self):
        pass

    def delete(self):
        pass

    @property
    def link(self):
        return url_for("files.view", key=self.record.key)

    @property
    def raw(self):
        return url_for("files.view_raw", key=self.record.key, filename=self.record.name)

    @property
    def data(self):
        return self.record
