from spice import app

handlers = {}

class Handler:
  def web_path():
    return app.config['UPLOAD_WEB_PATH']

  def process(record):
    pass

  def remove(record):
    pass

  def html(record):
    return ''


class ImageHandler(Handler):
  def html(record):
    return '<img src="%s">' % web_path(record.


def get_handler(extension):
  if extension in handler:
    return handler[extension]
  return default_handler




