import _mysql

class Worker:

    def __init__(self):
        self.db = None

    def work(self):
        self.db = _mysql.connect(host="localhost",user="root",passwd="",db="webaudit")
        self.db.query("""SELECT * FROM scans WHERE scans.`status`= 0""")

        r = self.db.store_result()


        for row in r.fetch_row(maxrows=0,how=1):
            print(row["id"])


	self.db.close()

worker = Worker();
worker.work();