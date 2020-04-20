from . import rdat

def get_records():
    return _rdb.get_records()

_rdb = rdat.RecordDatabase()
