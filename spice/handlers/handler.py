from spice import app

class DefaultHandler:
  type = 'default'
  extensions = []
  upload_path = app.config['UPLOAD_FOLDER']
  web_path = app.config['UPLOAD_WEB_PATH']
  cache_path = app.config['CACHE_FOLDER']
  cache_web_path = app.config['CACHE_WEB_PATH']
  template = 'view.html'

  def __init__(self, record):
    self.record = record

  def process(self):
    pass

  def delete(self):
    pass

  @property
  def link(self):
    return "%s/%s" % (self.web_path, self.record.filename)

  @property
  def raw(self):
    return "/%s/%s" % (self.record.key, self.record.name)

  @property
  def data(self):
    return self.record
