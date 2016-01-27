from abc import ABCMeta, abstractmethod


class WebTest(metaclass=ABCMeta):

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def status(self):
        pass

    @abstractmethod
    def stop(self):
        pass