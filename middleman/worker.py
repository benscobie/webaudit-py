import configparser
import pymysql.cursors

class Worker:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.db = None

    def work(self):
        self.db = pymysql.connect(host=self.config['DATABASE']['Server'],user=self.config['DATABASE']['Username'],passwd=self.config['DATABASE']['Password'],db=self.config['DATABASE']['Database'])
        cursor = self.db.cursor(pymysql.cursors.DictCursor)

        try:
            sql = "SELECT * FROM scans WHERE scans.`status`= 0"
            cursor.execute(sql)

            rows = cursor.fetchall()

            for row in rows:
                print(row["id"])

        finally:
            self.db.close()


worker = Worker();
worker.work();