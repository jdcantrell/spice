from spice.handlers.handler import DefaultHandler


class VideoHandler(DefaultHandler):
    type = 'videos'
    template = 'views/videos.html'
    extensions = ['.avi', '.m4v', '.ogv', '.webm', '.mov']

    # grab thumbnail?
    # def process(self):
