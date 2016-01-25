import db

class Workman:

    def __init__(self, site_id, site_url):
        self.site_id = site_id
        self.site_url = site_url
        self.db = db.get_connection()
        self.scan()

    def scan(self):
        print(self.site_url)