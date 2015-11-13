import _mysql

class Worker:

    def __init__(self):
        self.db = None

    def __del__(self):
        self.db.close()

    def work(self):
        self.db = _mysql.connect(host="localhost",user="root",passwd="",db="college_webaudit")
        self.db.query("""SELECT * FROM scans WHERE scans.`status`= 0""")

        r = self.db.store_result()

        for row in r.fetch_row(maxrows=0):
            print(row[0])




