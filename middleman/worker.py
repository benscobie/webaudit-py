import _mysql

class Worker:
    def init(self):
        db=_mysql.connect(host="localhost",user="root",passwd="",db="college_webaudit")


    def work(self):
        db.query("SELECT * FROM scans WHERE scans.`status`= 0");

        r=db.use_result();


