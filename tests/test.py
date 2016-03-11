from abc import ABCMeta, abstractmethod


class WebTest(metaclass=ABCMeta):

    @abstractmethod
    def run(self):
        pass
