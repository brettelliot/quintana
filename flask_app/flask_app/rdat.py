from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Date, Integer, Numeric
import os
from datetime import datetime, timedelta, date
from dataclasses import dataclass
from . import app
from decimal import Decimal
import flask.json

# jsonify doesn't naturally turn certain types into json. Use
# this custom encoder to specify how to encode those types.
class MyJSONEncoder(flask.json.JSONEncoder):

    def default(self, obj):
        if type(obj) == Decimal:
            # Convert decimal instances to floats.
            return float(obj)
        elif type(obj) == timedelta:
            # Convert timedeltas to strings
            return str(o)
        elif type(obj) == datetime:
            # Convert datetimes to strings
            return o.isoformat()
        elif type(obj) == date:
            return obj.isoformat()

        return super(MyJSONEncoder, self).default(obj)

app.json_encoder = MyJSONEncoder

# TODO Put all this stuff in a class
user = os.environ['POSTGRES_USER']
password = os.environ['POSTGRES_PASSWORD']
host = os.environ['POSTGRES_HOST']
database = os.environ['POSTGRES_DB']
port = os.environ['POSTGRES_PORT']

DATABASE_CONNECTION_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'

engine = create_engine(DATABASE_CONNECTION_URI)

# use session_factory() to get a new Session
_SessionFactory = sessionmaker(bind=engine)

Base = declarative_base()

def session_factory():
    Base.metadata.create_all(engine)
    return _SessionFactory()

@dataclass
class Record(Base):
    # These tell jsonify how to serialize this class
    id: int
    str_val: str
    date_val: datetime
    int_val: int
    num_val: Decimal

    __tablename__ = 'rdat_records'
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
        session = session_factory()
        record_query = session.query(Record)
        session.close()
        return record_query.all()

    def _create_records(self):
        session = session_factory()
        r1 = Record("str val 1", datetime(1984, 10, 20), 182, 84.5)
        r2 = Record("str val 2", datetime(1990, 5, 17), 173, 90)
        session.add(r1)
        session.add(r2)
        session.commit()
        session.close()
