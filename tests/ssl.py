from tests.test import WebTest
from models import Test, TestData, Scan
from database import db_session
from datetime import datetime
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from OpenSSL import SSL
import requests
import certifi
import ssl


class SSLTest(WebTest):

    def __init__(self, scan):
        self.scan = scan
        self.test = Test(scan_id=self.scan.id, name="SSL", status=1, started_date=datetime.utcnow())
        db_session.add(self.test)
        db_session.commit()

    def run(self):
        valid_ssl_cert = True

        try:
            requests.get(self.scan.website.get_url(), verify=certifi.where())
        except requests.exceptions.SSLError:
            valid_ssl_cert = False

        self.add_test_data(key="SSL_VALID_CERTIFICATE", value=valid_ssl_cert)

        self.ssl_version_check(SSL.SSLv2_METHOD, Ssl2HttpAdapter(), "SSL_SSLV2_ENABLED")
        self.ssl_version_check(SSL.SSLv3_METHOD, Ssl3HttpAdapter(), "SSL_SSLV3_ENABLED")
        self.ssl_version_check(SSL.TLSv1_METHOD, Tls1HttpAdapter(), "SSL_TLSV1_ENABLED")
        self.ssl_version_check(SSL.TLSv1_1_METHOD, Tls11HttpAdapter(), "SSL_TLSV11_ENABLED")
        self.ssl_version_check(SSL.TLSv1_2_METHOD, Tls12HttpAdapter(), "SSL_TLSV12_ENABLED")

        self.finish(status=2)

    def finish(self, status):
        self.test.finished_date=datetime.utcnow()
        self.test.status = status
        db_session.commit()
        if status == 3:
            return False
        return True

    def ssl_version_check(self, method, adapter, test_data_key):
        method_enabled = 1

        try:
            SSL.Context(method=method)
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            session = requests.Session()
            session.mount(self.scan.website.get_url(),adapter)
            try:
                response = session.get(self.scan.website.get_url(), verify=False)
            except requests.exceptions.SSLError:
                method_enabled = 0
        except ValueError:
            # OpenSSL method not supported by us (our problem)
            method_enabled = 2

        self.add_test_data(key=test_data_key, value=method_enabled)


class Ssl2HttpAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_version=ssl.PROTOCOL_SSLv2)


class Ssl3HttpAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_version=ssl.PROTOCOL_SSLv3)


class Tls1HttpAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_version=ssl.PROTOCOL_TLSv1)


class Tls11HttpAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_version=ssl.PROTOCOL_TLSv1_1)


class Tls12HttpAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_version=ssl.PROTOCOL_TLSv1_2)