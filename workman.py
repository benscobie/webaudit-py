class Workman(object):

    def __init__(self, website):
        self.website = website

    def scan(self):
        print(self.website.url)