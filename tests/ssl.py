from tests.test import WebTest
from models import ScanData, Scan
from database import db_session
import requests
import time


class SSLTest(WebTest):
    DATA_TYPE_SSL = 2
    API_ENDPOINT = "https://api.ssllabs.com/api/v2/"

    def __init__(self, scan):
        self.scan = scan

    def run(self):
        # For testing options = { 'host': self.scan.website.get_url(), 'publish': 'off', 'startNew': 'off', 'fromCache': 'on', 'all': 'done', 'ignoreMismatch': 'on' }
        options = { 'host': self.scan.website.get_url(), 'publish': 'off', 'startNew': 'on', 'fromCache': 'off', 'all': 'done', 'ignoreMismatch': 'on' }
        results = self.api_request(options)
        options.pop('startNew')

        while results['status'] != 'READY' and results['status'] != 'ERROR':
            time.sleep(10)
            results = self.api_request(options)

        endpoints = results['endpoints']

        scan_data = ScanData(scan_id=self.scan.id, data_type=self.DATA_TYPE_SSL, key="SSL_ENDPOINT_COUNT", value=len(endpoints))
        db_session.add(scan_data)

        i = 0
        for endpoint in endpoints:
            i += 1
            grade = endpoint["grade"]
            ip_address = endpoint["ipAddress"]

            grade_scan_data = ScanData(scan_id=self.scan.id, data_type=self.DATA_TYPE_SSL, key="SSL_ENDPOINT_" + str(i) + "_GRADE", value=grade)
            ipaddress_scan_data = ScanData(scan_id=self.scan.id, data_type=self.DATA_TYPE_SSL, key="SSL_ENDPOINT_" + str(i) + "_IP", value=ip_address)
            db_session.add(grade_scan_data)
            db_session.add(ipaddress_scan_data)

        db_session.commit()

    def api_request(self, options):
        url = self.API_ENDPOINT + "analyze"
        try:
            response = requests.get(url, params=options)
        except requests.exception.RequestException as e:
            print(e)

        data = response.json()
        return data

    def status(self):
        pass

    def stop(self):
        pass

