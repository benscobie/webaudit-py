from tests.test import WebTest
from models import ScanData, Scan
from database import db_session
import requests


class HeaderTest(WebTest):

    match_headers = ['Server', 'X-Frame-Options', 'Content-Security-Policy', 'X-XSS-Protection', 'X-Content-Type-Options', 'Strict-Transport-Security']

    def __init__(self, scan):
        self.scan = scan

    def run(self):
        r = requests.get(self.scan.website.url)
        if r.status_code == requests.codes.ok:
            for header in r.headers:
                if header in self.match_headers:
                    header_scan_data = ScanData(scan_id=self.scan.id, key=header, value=r.headers[header])
                    db_session.add(header_scan_data)


            db_session.commit()

    def status(self):
        pass

    def stop(self):
        pass

