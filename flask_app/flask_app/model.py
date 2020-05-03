import sqlalchemy as sa
import datetime as dt
import json
from . import db
from iexfinance.stocks import Stock
import logging

class Financials(db.base()):
    __tablename__ = 'quintana_financials'
    symbol = sa.Column(sa.String, primary_key=True)
    financials = sa.Column(sa.String)
    fetch_date = sa.Column(sa.String)

    def __init__(self, symbol, financials, fetch_date):
        self.symbol = symbol
        self.financials = financials
        self.fetch_date = fetch_date

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
        result = self._get_financials_query(symbol)
        today_str = dt.datetime.today().strftime('%Y-%m-%d')
        if (result != None and
                'fetch_date' in result and
                result.fetch_date != None and
                result.fetch_date > today_str and
                'financials' in result and
                result.financials != None):
            # We got a result and its not stale
            return json.loads(result.financials)
        elif result != None:
            # We got a result but it's stale
            self._remove_financials(symbol)

        # Get new result and return it
        self._fetch_financials(symbol)
        result = self._get_financials_query(symbol)
        if (result != None
                and 'financials' in result
                and  result.financials != None):
            return json.loads(result.financials)
        else:
            return {}


    def _get_financials(self, symbol):
        session = db.session_factory()
        result = session.query(Financials).filter(
            Financials.symbol == symbol).one_or_none()
        session.close()
        if result == None:
            return None
        else:
            return json.loads(result.financials)

    def _get_financials_query(self, symbol):
        """Get a single row in the financials table for the symbol if it exists

        Args:
            symbol(str):
                The ticker symbol

        Returns:
            Query:
                A query object with columns from the financials table or none
        """
        session = db.session_factory()
        result = session.query(Financials).filter(
            Financials.symbol == symbol).one_or_none()
        session.close()
        if result == None:
            return None
        else:
            return result

    def _fetch_financials(self, symbol):
        """ Call multiple endpoints on IEX using iexfinance and write the
        results into our db."""
        try:
            raw_dict = {'symbol': symbol}
            stock = Stock(symbol)

            cash_flow = stock.get_cash_flow()
            if ('cashflow' in cash_flow and
                    len(cash_flow['cashflow']) > 0):
                raw_dict.update(cash_flow['cashflow'][0])
            else:
                logging.error('{} has no cash flow data'.format(symbol))

            income_statement_list = stock.get_income_statement()
            if len(income_statement_list) == 0:
                logging.error('{} has no income statement'.format(symbol))
            else:
                raw_dict.update(income_statement_list[0])

            bal_sheet = stock.get_balance_sheet()
            if ('balancesheet' in bal_sheet and
                    len(bal_sheet['balancesheet']) > 0):
                raw_dict.update(bal_sheet['balancesheet'][0])
            else:
                logging.error('{} has no balance sheet data'.format(symbol))

            key_stats_dict = stock.get_key_stats()
            if 'nextEarningsDate' in key_stats_dict:
                raw_dict['nextEarningsDate'] = key_stats_dict['nextEarningsDate']
            else:
                logging.error('{} has no next earnings date data'.format(symbol))

            if 'companyName' in key_stats_dict:
                raw_dict['companyName'] = key_stats_dict['companyName']
            else:
                logging.error('{} has no company name data'.format(symbol))

        except Exception as e:
            logging.error('Error in _fetch_financials')
            logging.error('symbol:' + symbol)
            logging.error(e)
            return
        else:
            today = dt.datetime.today()
            today_str = today.strftime('%Y-%m-%d')

            if('nextEarningsDate' in raw_dict and
                    raw_dict['nextEarningsDate'] is not None
                    and raw_dict['nextEarningsDate'] > today_str):
                fetch_date = raw_dict['nextEarningsDate']
            else:
                fetch_date = (today +
                              dt.timedelta(days=31)).strftime('%Y-%m-%d')

            session = db.session_factory()
            financial = Financials(symbol, json.dumps(raw_dict), fetch_date)
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
