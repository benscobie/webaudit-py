import db
import workman
import configparser
import threading
import pymysql.cursors

class Middleman:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.db = db.get_connection()
        self.scan_threads = []

    def process_queue(self):
        for thread in self.scan_threads:
            if not thread.is_alive():
                thread.handled = True

        self.scan_threads = [t for t in self.scan_threads if not t.handled]

        if len(self.scan_threads) < int(self.config["WEBAUDIT"]["MaxConcurrentScans"]):
            cursor = self.db.cursor(pymysql.cursors.DictCursor)

            try:
                sql = "SELECT * FROM scans WHERE scans.`status`= 0"
                cursor.execute(sql)
                rows = cursor.fetchall()

                for row in rows:
                    scan_thread = threading.Thread(target=self.init_scan, args=(row["id"], row["url"])).start()
                    self.scan_threads.append(scan_thread)

            finally:
                self.db.close()

    def init_scan(self, site_id, site_url):
        worker = workman.Workman(site_id, site_url)
        worker.scan();
