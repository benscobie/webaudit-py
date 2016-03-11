from abc import ABCMeta, abstractmethod
from database import db_session
from models import TestData

class WebTest(metaclass=ABCMeta):

    @abstractmethod
    def run(self):
        pass

    def add_test_data(self, key, value, data_type=None):
        test_data = TestData(test_id=self.test.id, key=key, value=value, data_type=data_type)
        db_session.add(test_data)
