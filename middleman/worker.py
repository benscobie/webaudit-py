import pymysql.cursors

class Worker:

    def __init__(self):
        self.db = None

    def work(self):
        self.db = pymysql.connect(host="localhost",user="root",passwd="",db="webaudit")
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