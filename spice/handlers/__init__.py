from handler import DefaultHandler
from text import TextHandler
from images import ImageHandler

handler_classes = [
  DefaultHandler,
  TextHandler,
  ImageHandler,
]

def get_handler(filetype):
  for h in handler_classes:
    if filetype in h.extensions:
      return h
  return Handler

def get_handler_instance(record):
  handler_data = get_handler(record.filetype)
  return handler_data(record)

