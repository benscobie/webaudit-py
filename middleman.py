import workman
import configparser
import time
import threading
from database import init_engine, db_session
from models import Scan
from datetime import datetime

class Middleman:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.max_scans = int(self.config["WEBAUDIT"]["MaxConcurrentScans"])

        #init_engine('mysql+pymysql://' + self.config['DATABASE']['Username'] + ':' + self.config['DATABASE']['Password'] + '@' + self.config['DATABASE']['Server'] + '/' + self.config['DATABASE']['Database'], pool_recycle=3600)
        self.scans_in_progress = dict()

    def run(self):
        while True:
            self.process_queue()
            self.process_running_scans()
            time.sleep(1)

    def process_running_scans(self):
        current_scans = len(self.scans_in_progress)
        if current_scans == 0:
            return

        print("Processing running scans [" + str(current_scans) + "/" + str(self.max_scans) + "]" , flush=True)
        finished_scans = [];

        for key, list in self.scans_in_progress.items():
            if not list['thread'].is_alive():
                finished_scans.append(key);

        for finished_scan in finished_scans:
            self.scans_in_progress.pop(finished_scan, None)

    def process_queue(self):
        print("Processing queue", flush=True)
        current_scans = len(self.scans_in_progress)
        slots_available = (self.max_scans - current_scans)

        if current_scans > 0:
            query = db_session.query(Scan).filter(Scan.status == 0).filter(~Scan.id.in_(self.scans_in_progress.keys())).order_by(Scan.created_date).limit(slots_available)
        else:
            query = db_session.query(Scan).filter(Scan.status == 0).order_by(Scan.created_date).limit(slots_available)

        if slots_available > 0:
            for scan in query:
                print("Scanning scan ID #" + str(scan.id), flush=True)
                scan_thread = threading.Thread(target=self.init_scan, args=(scan.id,))
                scan_thread.start()
                self.scans_in_progress[scan.id] = { 'thread': scan_thread }

        db_session.close()


    @staticmethod
    def init_scan(scan_id):
        worker = workman.Workman(scan_id)
        worker.start_scan()
