from tests.test import WebTest
from models import Test
from database import db_session
from datetime import datetime
from lxml import html
import requests


class SoftwareTest(WebTest):

    def __init__(self, scan):
        self.scan = scan

    def init(self):
        self.test = Test(scan_id=self.scan.id, name="HEADERS", status=0)
        db_session.add(self.test)
        db_session.commit()

    def run(self):
        self.test.status = 1
        self.test.started_date = datetime.utcnow()
        db_session.commit()

        try:
            response = requests.get(self.scan.website.get_url())
        except requests.exception.RequestException:
            return self.finish(status=3)

        tree = html.fromstring(response.content)
        meta_generator = tree.xpath('/html/head/meta[@name="generator"]/@content')
        print(meta_generator)

        return self.finish(status=2)

    def finish(self, status):
        self.test.finished_date=datetime.utcnow()
        self.test.status = status
        db_session.commit()
        if status == 3:
            return False

        return True
