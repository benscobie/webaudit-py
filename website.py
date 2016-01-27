class Website(object):

    def __init__(self, url):
        self.url = self.parse_url(url)

    def parse_url(self, url):
        return url