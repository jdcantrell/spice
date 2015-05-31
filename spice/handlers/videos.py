from handler import DefaultHandler


class VideoHandler(DefaultHandler):
    type = 'videos'
    template = 'views/videos.html'
    extensions = ['.avi', '.m4v', '.ogv', '.webm']

    # grab thumbnail?
    # def process(self):