import abc

class Test(object):
    __metaclass__  = abc.ABCMeta

    @abc.abstractmethod
    def run(self):
        """Method that should do something."""

    @abc.abstractmethod
    def status(self):
        """Method that should do something."""

    @abc.abstractmethod
    def stop(self):
        """Method that should do something."""