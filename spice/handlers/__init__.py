from flask import current_app
from .handler import DefaultHandler
from .text import TextHandler
from .images import ImageHandler
from .gif import GifHandler
from .videos import VideoHandler
from .audio import AudioHandler

handler_classes = [
    DefaultHandler,
    TextHandler,
    ImageHandler,
    GifHandler,
    VideoHandler,
    AudioHandler,
]


def get_handler(filetype):
    for h in handler_classes:
        if filetype in h.extensions:
            return h
    return DefaultHandler


def get_handler_instance(record):
    handler_data = get_handler(record.filetype)

    return handler_data(
        record, current_app.config["CACHE_FOLDER"], current_app.config["UPLOAD_FOLDER"]
    )
