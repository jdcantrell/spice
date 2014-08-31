from handler import DefaultHandler
from wand.image import Image

class ImageHandler(DefaultHandler):
  type = 'images'
  template = 'views/images.html'
  extensions = ['.png', '.jpg', '.gif', '.bmp']

  def process(self):
    image = Image(filename='%s/%s' % (self.upload_path, self.record.filename))
    ratio = float(image.width) / float(image.height)
    height = image.height
    width = image.width

    if image.height > 215:
      height = 215
      width = int(215.0 * ratio)

    if width > 700:
      width = 700
      height = int(700.0 / ratio)

    image.resize(width, height)
    image.save(filename=self.thumbnail_file)

  @property
  def thumbnail_file(self):
    return '%s/thumbnail-%s' % (self.cache_path, self.record.filename)

  @property
  def thumbnail(self):
    return '%s/thumbnail-%s' % (self.cache_web_path, self.record.filename)
