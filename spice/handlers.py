from spice import app

class Handler:
  @staticmethod
  def web_path():
    return app.config['UPLOAD_WEB_PATH']

  @staticmethod
  def process(record):
    pass

  @staticmethod
  def remove(record):
    pass

  @staticmethod
  def html(record):
    return ''


class ImageHandler(Handler):

  @staticmethod
  def html(record):
    return '<img src="%s/%s">' % (Handler.web_path(), record.filename)


handlers = {
  'images': {
    'name': 'images',
    'extensions': ['.png', '.jpg', '.gif', '.bmp'],
    'class': ImageHandler
   }
}


def get_handler(extension):
  global handlers
  for key in handlers.keys():
    handler = handlers[key]
    if extension in handler['extensions']:
      return handler
  return 'default'
