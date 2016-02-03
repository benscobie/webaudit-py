import workman
import configparser
import time
import threading
from database import init_engine, db_session
from models import Scan


class Middleman:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        #init_engine('mysql+pymysql://' + self.config['DATABASE']['Username'] + ':' + self.config['DATABASE']['Password'] + '@' + self.config['DATABASE']['Server'] + '/' + self.config['DATABASE']['Database'], pool_recycle=3600)
        self.scans_in_progress = dict()

    def run(self):
        while True:
            self.process_running_scans()
            self.process_queue()
            time.sleep(5)

    def process_running_scans(self):
        print("Processing running scans", flush=True)
        finished_scans = [];

        for key, list in self.scans_in_progress.items():
            if not list['thread'].is_alive():
                finished_scans.append(key);

        for finished_scan in finished_scans:
            scan = self.scans_in_progress[finished_scan]['scan']
            scan.status = 1
            db_session.commit()
            del self.scans_in_progress[finished_scan]

    def process_queue(self):
        print("Processing queue", flush=True)
        max_scans = int(self.config["WEBAUDIT"]["MaxConcurrentScans"])
        current_scans = len(self.scans_in_progress)
        slots_available = (max_scans - current_scans)

        if slots_available > 0:
            for scan in db_session.query(Scan).filter(Scan.status == 0).filter(~Scan.id.in_(self.scans_in_progress.keys())).order_by(Scan.created_date).limit(slots_available):
                print("Scanning scan ID #" + str(scan.id), flush=True)
                scan_thread = threading.Thread(target=self.init_scan, args=(scan,))
                scan_thread.start()
                self.scans_in_progress[scan.id] = { 'scan': scan, 'thread': scan_thread }

    @staticmethod
    def init_scan(scan):
        worker = workman.Workman(scan)
        worker.start_scan()
