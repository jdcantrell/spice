import json

from flask import url_for
from spice.handlers.handler import DefaultHandler
from wand.image import Image


class ImageHandler(DefaultHandler):
    type = 'images'
    template = 'views/images.html'
    extensions = ['.png', '.jpg', '.gif', '.bmp']

    def __init__(self, record):
        self.record = record
        try:
            self.extra = json.loads(record.extra)
        except:
            self.extra = {}

    def process(self):
        image = Image(
            filename='%s/%s' % (self.upload_path, self.record.filename)
        )

        ratio = float(image.width) / float(image.height)
        height = image.height
        width = image.width

        if image.height > 400:
            height = 400
            width = int(400.0 * ratio)

        if width > 700:
            width = 700
            height = int(700.0 / ratio)

        self.record.extra = json.dumps({
            'height': image.height,
            'width': image.width,
            'thumb': {
                'height': width,
                'width': height,
            },
        })

        image.resize(width, height)
        image.save(filename=self.thumbnail_file)

    @property
    def thumb_size(self):
        return self.extra['thumb']

    @property
    def size(self):
        return self.extra

    @property
    def thumbnail_file(self):
        return '%s/thumbnail-%s' % (self.cache_path, self.record.filename)

    @property
    def thumbnail(self):
        return url_for('static', filename='cache/thumbnail-%s' % (self.record.filename))
