from tests.test import WebTest
from models import Test, TestData, Scan
from database import db_session
from datetime import datetime
import requests
import time


class SSLAPITest(WebTest):
    API_ENDPOINT = "https://api.ssllabs.com/api/v2/"

    def __init__(self, scan):
        self.scan = scan
        self.test = Test(scan_id=self.scan.id, name="SSLAPI", status=1, started_date=datetime.utcnow())
        db_session.add(self.test)
        db_session.commit()

    def run(self):
        if not self.api_check():
            return self.finish(status=3)

        #options = { 'host': self.scan.website.get_url(), 'publish': 'off', 'startNew': 'off', 'fromCache': 'on', 'all': 'done', 'ignoreMismatch': 'on' }
        options = {'host': self.scan.website.get_url(), 'publish': 'off', 'startNew': 'on', 'fromCache': 'off', 'all': 'done', 'ignoreMismatch': 'on'}

        results = self.api_request(options)

        if results == False:
            return self.finish(status=3)

        options.pop('startNew')

        while results == False or (results['status'] != 'READY' and results['status'] != 'ERROR'):
            time.sleep(10)
            results = self.api_request(options)

        endpoints = results['endpoints']
        self.add_test_data(key="SSL_ENDPOINT_COUNT", value=len(endpoints))

        i = 0
        for endpoint in endpoints:
            i += 1
            grade = endpoint["grade"]
            ip_address = endpoint["ipAddress"]
            self.add_test_data(key="SSL_ENDPOINT_" + str(i) + "_GRADE", value=grade)
            self.add_test_data(key="SSL_ENDPOINT_" + str(i) + "_IP", value=ip_address)

        self.finish(status=2)

    def api_request(self, options):
        url = self.API_ENDPOINT + "analyze"
        try:
            response = requests.get(url, params=options)
        except requests.exception.RequestException:
            return False

        data = response.json()
        return data

    def api_check(self):
        url = self.API_ENDPOINT + "info"
        try:
            response = requests.get(url)
        except requests.exception.RequestException:
            return False;

        if response.status_code != requests.codes.ok:
            return False;

        response = response.json()

        if response.get('maxAssessments') <= 0:
            return False;

        return True;

    def finish(self, status):
        self.test.finished_date=datetime.utcnow()
        self.test.status = status
        db_session.commit()
        if status == 3:
            return False
        return True