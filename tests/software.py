from tests.test import WebTest
from models import Test, TestData, Scan
from database import db_session
from datetime import datetime
import requests


class HeaderTest(WebTest):

    def __init__(self, scan):
        self.scan = scan
        self.test = Test(scan_id=self.scan.id, name="HEADERS", status=1, started_date=datetime.utcnow())
        db_session.add(self.test)
        db_session.commit()

    def run(self):
        try:
            response = requests.get(self.scan.website.get_url())
        except requests.exception.RequestException:
            return self.finish(status=3)

        if response.status_code == requests.codes.ok:
            for header in response.headers:
                if header in self.match_headers:
                    self.add_test_data(key=header, value=response.headers[header])

        return self.finish(status=2)

    def finish(self, status):
        self.test.finished_date=datetime.utcnow()
        self.test.status = status
        db_session.commit()
        if status == 3:
            return False

        return True
