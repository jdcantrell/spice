from spice.handlers.handler import DefaultHandler
from spice.handlers.text import TextHandler
from spice.handlers.images import ImageHandler
from spice.handlers.videos import VideoHandler

handler_classes = [
    DefaultHandler,
    TextHandler,
    ImageHandler,
    VideoHandler
]


def get_handler(filetype):
    for h in handler_classes:
        if filetype in h.extensions:
            return h
    return DefaultHandler


def get_handler_instance(record):
    handler_data = get_handler(record.filetype)
    return handler_data(record)
