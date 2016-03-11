from tests.test import WebTest
from models import Test, TestData, Scan
from database import db_session
from datetime import datetime
import requests


class HeaderTest(WebTest):
    DATA_TYPE_HEADER = 1

    match_headers = [
        'Server',
        'X-Frame-Options',
        'Content-Security-Policy',
        'X-XSS-Protection',
        'X-Content-Type-Options',
        'Strict-Transport-Security'
    ]

    def __init__(self, scan):
        self.scan = scan
        self.test = Test(scan_id=self.scan.id, name="HEADERS", status=1, started_date=datetime.utcnow())
        db_session.add(self.test)
        db_session.commit()

    def run(self):
        r = requests.get(self.scan.website.get_url())
        if r.status_code == requests.codes.ok:
            for header in r.headers:
                if header in self.match_headers:
                    header_test_data = TestData(test_id=self.test.id, data_type=self.DATA_TYPE_HEADER, key=header, value=r.headers[header])
                    db_session.add(header_test_data)
            db_session.commit()

        self.finish()

    def finish(self):
        self.test.finished_date=datetime.utcnow()
        self.test.status = 2
        db_session.commit()
