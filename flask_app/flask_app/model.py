from sqlalchemy import Column, String, Date, Integer, Numeric
from datetime import datetime, timedelta, date
from dataclasses import dataclass
from decimal import Decimal
from . import app
from . import db

@dataclass
class Record(db.base()):
    # These tell jsonify how to serialize this class
    id: int
    str_val: str
    date_val: datetime
    int_val: int
    num_val: Decimal

    __tablename__ = 'juniper_records'
    id = Column(Integer, primary_key=True)
    str_val = Column(String)
    date_val = Column(Date)
    int_val = Column(Integer)
    num_val = Column(Numeric)

    def __init__(self, str_val, date_val, int_val, num_val):
        self.str_val = str_val
        self.date_val = date_val
        self.int_val = int_val
        self.num_val = num_val

class RecordDatabase:

    def __init__(self):
        pass

    def get_records(self):
        records = self._get_records()
        if len(records) == 0:
            self._create_records()
        records = self._get_records()
        return records

    def _get_records(self):
        #with db.session_scope() as session:
        #    record_query = session.query(Record)
        #return record_query.all()
        #
        session = db.session_factory()
        record_query = session.query(Record)
        session.close()
        return record_query.all()

    def _create_records(self):
        #with db.session_scope() as session:
        #    r1 = Record("str val 1", datetime(1984, 10, 20), 182, 84.5)
        #    r2 = Record("str val 2", datetime(1990, 5, 17), 173, 90)
        #    session.add(r1)
        #    session.add(r2)
        #
        session = db.session_factory()
        r1 = Record("str val 1", datetime(1984, 10, 20), 182, 84.5)
        r2 = Record("str val 2", datetime(1990, 5, 17), 173, 90)
        session.add(r1)
        session.add(r2)
        session.commit()
        session.close()

def get_records():
    return _rdb.get_records()

_rdb = RecordDatabase()
