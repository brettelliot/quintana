import sqlalchemy as sa
import datetime as dt
import json
from . import db
from iexfinance.stocks import Stock

class Financials(db.base()):
    __tablename__ = 'quintana_financials'
    symbol = sa.Column(sa.String, primary_key=True)
    financials = sa.Column(sa.String)

    def __init__(self, symbol, financials):
        self.symbol = symbol
        self.financials = financials

class QuintanaDatabase:

    def __init__(self):
        pass

    def get_financials(self, symbol):
        """ Returns dict of financial data for a stock symbol.

        Args:
            symbol (str):
                The ticker symbol of the stock

        Returns:
            dict:
                A dict containing the financial data

        """
        result = self._get_financials(symbol)
        today_str = dt.datetime.today().strftime('%Y-%m-%d')
        if result != None and result['nextEarningsDate'] >= today_str:
            # We got a result and its not stale
            return result
        elif result != None:
            # We got a result but it's stale
            self._remove_financials(symbol)

        # Get new result and return it
        self._fetch_financials(symbol)
        return self._get_financials(symbol)

    def _get_financials(self, symbol):
        session = db.session_factory()
        result = session.query(Financials).filter(
            Financials.symbol == symbol).one_or_none()
        session.close()
        if result == None:
            return None
        else:
            return json.loads(result.financials)

    def _fetch_financials(self, symbol):
        """ Call multiple endpoints on IEX using iexfinance and write the
        results into our db."""
        try:
            stock = Stock(symbol)
            raw_dict = stock.get_cash_flow()['cashflow'][0]
            raw_dict.update(stock.get_income_statement()[0])
            raw_dict.update(stock.get_balance_sheet()['balancesheet'][0])
            raw_dict['nextEarningsDate'] = stock.get_key_stats()['nextEarningsDate']
            raw_dict['companyName'] = stock.get_key_stats()['companyName']
            raw_dict['symbol'] = symbol
        except Exception as e:
            print(e)
            return
        else:
            session = db.session_factory()
            financial = Financials(symbol, json.dumps(raw_dict))
            session.add(financial)
            session.commit()
            session.close()

    def _remove_financials(self, symbol):
        session = db.session_factory()
        session.query(Financials).filter(Financials.symbol == symbol).delete()
        session.commit()
        session.close()

def get_financials(symbol):
    return _qdb.get_financials(symbol)

_qdb = QuintanaDatabase()
