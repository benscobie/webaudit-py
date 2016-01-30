import workman
import configparser
from database import init_engine, db_session
from models import Scan

import threading

class Middleman:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        #init_engine('mysql+pymysql://' + self.config['DATABASE']['Username'] + ':' + self.config['DATABASE']['Password'] + '@' + self.config['DATABASE']['Server'] + '/' + self.config['DATABASE']['Database'], pool_recycle=3600)
        self.scan_threads = []

    def process_queue(self):
        for thread in self.scan_threads:
            if not thread.is_alive():
                thread.handled = True

        self.scan_threads = [t for t in self.scan_threads if not t.handled]

        maxScans = int(self.config["WEBAUDIT"]["MaxConcurrentScans"])
        currentScans = len(self.scan_threads)
        slotsAvailable = (maxScans - currentScans)

        if slotsAvailable > 0:
            for scan in db_session.query(Scan).order_by(Scan.created_date).limit(slotsAvailable):
                scan_thread = threading.Thread(target=self.init_scan, args=(scan,)).start()
                self.scan_threads.append(scan_thread)


    def init_scan(self, scan):
        worker = workman.Workman(scan)
        worker.start_scan()
