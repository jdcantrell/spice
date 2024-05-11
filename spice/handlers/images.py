import json

from flask import url_for
from spice.handlers.handler import DefaultHandler
from PIL import Image, ImageSequence


class ImageHandler(DefaultHandler):
    type = "images"
    template = "views/images.html"
    extensions = [".png", ".jpg", ".gif", ".bmp"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        try:
            self.extra = json.loads(self.record.extra)
        except:
            self.extra = {}

    def process(self):
        image = Image.open("%s/%s" % (self.upload_path, self.record.filename))

        ratio = float(image.width) / float(image.height)
        height = image.height
        width = image.width

        if image.height > 400:
            height = 400
            width = int(400.0 * ratio)

        if width > 700:
            width = 700
            height = int(700.0 / ratio)

        self.record.extra = json.dumps(
            {
                "height": image.height,
                "width": image.width,
                "thumb": {"height": width, "width": height},
            }
        )

        if "version" in image.info and b"GIF" in image.info["version"]:
            frameset = ImageSequence.Iterator(image)
            frames = []
            for frame in frameset:
                thumbnail = frame.copy()
                thumbnail.thumbnail((width, height))
                frames.append(thumbnail)

            image.thumbnail((width, height))
            thumb = frames.pop(0)
            thumb.info = image.info
            thumb.save(
                self.thumbnail_file,
                save_all=True,
                append_images=frames,
                duration=image.info.get("duration", 3),
                loop=image.info.get("loop", 0),
            )
        else:
            image.thumbnail((width, height))
            image.save(self.thumbnail_file, "WebP", quality=85)

    @property
    def thumb_size(self):
        return self.extra["thumb"]

    @property
    def size(self):
        return self.extra

    @property
    def thumbnail_file(self):
        # fix gif
        return "%s/thumbnail-%s.webp" % (self.cache_path, self.record.filename)

    @property
    def thumbnail(self):
        return url_for("static", filename="cache/thumbnail-%s.webp" % (self.record.filename))
