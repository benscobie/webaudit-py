from tests.headers import HeaderTest

class Workman(object):

    def __init__(self, scan):
        self.scan = scan

    def start_scan(self):
        print(self.scan.website.url)
        header = HeaderTest(self.scan)
        header.run()