import abc
from six import with_metaclass

__version__= "$Id: loop.py 25 2018-01-26 19:00:40Z lbusoni $"


class Loop(with_metaclass(abc.ABCMeta, object)):

    @abc.abstractmethod
    def name(self):
        assert False


    @abc.abstractmethod
    def close(self):
        assert False


    @abc.abstractmethod
    def open(self):
        assert False


    @abc.abstractmethod
    def isClosed(self):
        assert False


    @abc.abstractmethod
    def performOnePass(self):
        assert False


    @abc.abstractmethod
    def getConvergenceStepCount(self):
        assert False


    @abc.abstractmethod
    def hasConverged(self):
        assert False



class LoopException(Exception):

    def __init__(self, message):
        Exception.__init__(self, message)
