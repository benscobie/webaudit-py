from abc import ABCMeta, abstractmethod
from database import db_session
from models import TestData

class WebTest(metaclass=ABCMeta):

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def run(self):
        pass

    def add_test_data(self, key=None, value=None, data_type=None, kvdata=None):
        if key is not None and value is not None:
            test_data = TestData(test_id=self.test.id, key=key, value=value, data_type=data_type)
            db_session.add(test_data)

        if kvdata is not None:
            for key, value in kvdata.items():
                test_data = TestData(test_id=self.test.id, key=key, value=value)
                db_session.add(test_data)
