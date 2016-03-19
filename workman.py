from tests.headers import HeaderTest
from tests.ssl import SSLTest
from tests.software import SoftwareTest
from database import db_session
from models import Scan
from datetime import datetime


class Workman(object):

    def __init__(self, scan_id):
        # Load scan object inside thread as SQLAlchemy? has issues with passing in objects from other threads
        self.scan = db_session.query(Scan).get(scan_id)
        self.scan.started_date = datetime.utcnow()
        self.scan.status = 1
        db_session.commit()

    def start_scan(self):
        print(self.scan.website.get_url())

        header_test = HeaderTest(self.scan)
        #software_test = SoftwareTest(self.scan)
        ssl_test = SSLTest(self.scan);

        header_test.init()
        #software_test.init()
        if self.scan.website.protocol == "https":
            ssl_test.init()

        header_test.run()
        #software_test.run()

        if self.scan.website.protocol == "https":
            ssl_test.run()

        self.finish_scan()

    def finish_scan(self):
        self.scan.finished_date = datetime.utcnow()
        self.scan.status = 2
        db_session.commit()
        return