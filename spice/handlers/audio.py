from spice.handlers.handler import DefaultHandler


class AudioHandler(DefaultHandler):
    type = "audio"
    template = "views/audio.html"
    extensions = [".mp3", ".ogg", ".flac", ".wav"]

    # grab thumbnail?
    # def process(self):
