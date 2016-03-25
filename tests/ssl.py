from tests.test import WebTest
from models import Test
from database import db_session
from datetime import datetime
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import OpenSSL
import requests
import certifi
import ssl


class SSLTest(WebTest):

    def __init__(self, scan):
        self.scan = scan

    def init(self):
        self.test = Test(scan_id=self.scan.id, name="SSL", status=0)
        db_session.add(self.test)
        db_session.commit()

    def run(self):
        self.test.status = 1
        self.test.started_date = datetime.utcnow()
        db_session.commit()

        valid_ssl_cert = True

        try:
            requests.get(self.scan.website.get_url(), verify=certifi.where())
        except requests.exceptions.SSLError:
            valid_ssl_cert = False
        except requests.exceptions.RequestException:
            return self.finish(status=3)

        self.add_test_data(key="VALID_CERTIFICATE", value=valid_ssl_cert)

        usable_best_protocol = ssl.PROTOCOL_SSLv3
        if self._ssl_version_check(OpenSSL.SSL.SSLv2_METHOD, Ssl2HttpAdapter(), "SSLV2_ENABLED"):
            usable_best_protocol = ssl.PROTOCOL_SSLv2
        if self._ssl_version_check(OpenSSL.SSL.SSLv3_METHOD, Ssl3HttpAdapter(), "SSLV3_ENABLED"):
            usable_best_protocol = ssl.PROTOCOL_SSLv3
        if self._ssl_version_check(OpenSSL.SSL.TLSv1_METHOD, Tls1HttpAdapter(), "TLSV1_ENABLED"):
            usable_best_protocol = ssl.PROTOCOL_TLSv1
        if self._ssl_version_check(OpenSSL.SSL.TLSv1_1_METHOD, Tls11HttpAdapter(), "TLSV11_ENABLED"):
            usable_best_protocol = ssl.PROTOCOL_TLSv1_1
        if self._ssl_version_check(OpenSSL.SSL.TLSv1_2_METHOD, Tls12HttpAdapter(), "TLSV12_ENABLED"):
            usable_best_protocol = ssl.PROTOCOL_TLSv1_2

        try:
            cert = ssl.get_server_certificate((self.scan.website.hostname, 443),ssl_version=usable_best_protocol)
            x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)

            algo = x509.get_signature_algorithm().decode('ascii')
            strength = x509.get_pubkey().bits()
            common_name = x509.get_subject().commonName
            issuer = x509.get_issuer().commonName
            valid_from = datetime.strptime(x509.get_notBefore().decode('ascii'), '%Y%m%d%H%M%SZ')
            valid_to = datetime.strptime(x509.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ')

            data_array = {
                "SIGNATURE_ALGORITHM": algo,
                "KEY_STRENGTH": strength,
                "COMMON_NAME": common_name,
                "ISSUER": issuer,
                "VALID_FROM": valid_from,
                "VALID_TO": valid_to
            }

            self.add_test_data(kvdata=data_array)

        except ssl.SSLError as e:
            print(e, flush=True)

        self.finish(status=2)

    def finish(self, status):
        self.test.finished_date=datetime.utcnow()
        self.test.status = status
        db_session.commit()
        if status == 3:
            return False
        return True

    def _ssl_version_check(self, method, adapter, test_data_key):
        method_enabled = 1

        try:
            OpenSSL.SSL.Context(method=method)
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            session = requests.Session()
            session.mount(self.scan.website.get_url(),adapter)
            try:
                response = session.get(self.scan.website.get_url(), verify=False)
            except requests.exceptions.SSLError:
                method_enabled = 0
            except requests.exceptions.RequestException:
                method_enabled = 2
        except ValueError:
            # OpenSSL method not available (our problem)
            method_enabled = 2

        self.add_test_data(key=test_data_key, value=method_enabled)

        return method_enabled == 1


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