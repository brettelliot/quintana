from sqlalchemy import Column, String, Date, Integer, Numeric
from datetime import datetime, timedelta, date
from dataclasses import dataclass
from decimal import Decimal
from . import app
from . import db

@dataclass
class Financials(db.base()):
    # These tell jsonify how to serialize this class
    symbol: str
    financials: str
    next_earnings_date: str

    __tablename__ = 'quintana_financials'
    symbol = Column(String, primary_key=True)
    financials = Column(String)
    next_earnings_date = Column(String)

    def __init__(self, symbol, financials, next_earnings_date):
        self.symbol = symbol
        self.financials = financials
        self.next_earnings_date = next_earnings_date

class QuintanaDatabase:

    def __init__(self):
        pass

    def get_financials(self):
        financials = self._get_financials()
        if len(financials) == 0:
            self._create_financials()
        financials = self._get_financials()
        return financials

    def _get_financials(self):
        session = db.session_factory()
        financial_query = session.query(Financials)
        session.close()
        return financial_query.all()

    def _create_financials(self):
        ex1_json = '{"results":[{"symbol": "ex1","reportDate": "2017-03-31", \
                "fiscalDate": "2017-03-31","currentCash": 25913000000}]}'
        ex2_json = '{"results":[{"symbol": "ex2","reportDate": "2018-06-30", \
                "fiscalDate": "2018-06-30","currentCash": 59913000000}]}'

        session = db.session_factory()
        ex1 = Financials("ex1", ex1_json, "2020-04-30")
        ex2 = Financials("ex2", ex2_json, "2020-05-21")
        session.add(ex1)
        session.add(ex2)
        session.commit()
        session.close()

def get_financials():
    return _qdb.get_financials()

_qdb = QuintanaDatabase()
