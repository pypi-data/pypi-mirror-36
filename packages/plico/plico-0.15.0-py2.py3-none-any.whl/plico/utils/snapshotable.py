import abc
import pyfits
from six import with_metaclass

__version__= "$Id: snapshotable.py 25 2018-01-26 19:00:40Z lbusoni $"


class Snapshotable(with_metaclass(abc.ABCMeta, object)):
    @abc.abstractmethod
    def getSnapshot(self, prefix):
        assert False


    @staticmethod
    def _isSuitableForFITSHeader(value):
        return value is not None


    @staticmethod
    def _truncateStringIfAny(key, value):
        maxValueLenInChars= 67 - len(key)
        if len(value) > maxValueLenInChars:
            return value[0:maxValueLenInChars]
        return value


    @staticmethod
    def _updateHeader(hdr, key, value):
        MAX_KEY_LEN_CHARS= 59
        assert len(key) <= MAX_KEY_LEN_CHARS
        if isinstance(value, str):
            value= Snapshotable._truncateStringIfAny(key, value)
        hdr.update({'hierarch '+ key: value})


    @staticmethod
    def asFITSHeader(snapshotDictionary):
        hdr= pyfits.Header()
        for k in sorted(snapshotDictionary.keys()):
            value= snapshotDictionary[k]
            if Snapshotable._isSuitableForFITSHeader(value):
                Snapshotable._updateHeader(hdr, k, value)
        return hdr


    @staticmethod
    def prepend(prefix, snapshotDict):
        assert len(prefix) > 0, "Prefix length must be greater than zero"
        for each in list(snapshotDict.keys()):
            value= snapshotDict[each]
            del snapshotDict[each]
            newKey= prefix + "." + each
            snapshotDict[newKey]= value
        return snapshotDict


    @staticmethod
    def fromFITSHeader(hdr):
        snapshot= {}
        for each in hdr:
            snapshot[each]= hdr[each]
        return snapshot


    @staticmethod
    def removeEntriesWithValueNone(snapshotDict):
        for each in list(snapshotDict.keys()):
            if snapshotDict[each] is None:
                del snapshotDict[each]
