import sqlalchemy as sa
import datetime as dt
import json
from . import db
from . import myjinxstock
import logging

class Financials(db.base()):
    __tablename__ = 'quintana_financials'
    symbol = sa.Column(sa.String, primary_key=True)
    financials = sa.Column(sa.String)
    report_date = sa.Column(sa.String)
    last_check_date = sa.Column(sa.String)

    def __init__(self, symbol, financials, report_date, last_check_date):
        self.symbol = symbol
        self.financials = financials
        self.report_date = report_date
        self.last_check_date = last_check_date

class QuintanaDatabase:

    def __init__(self):
        pass

    def get_financials(self, symbol):
        """ Returns dict of financial data for a stock symbol.

        Parameters
        ----------
        symbol: str
            The ticker symbol of the stock

        Returns
        -------
        data: dict:
            A dict containing the financial data
        """
        # First, see try and get something from the db
        result = self._get_financials_query(symbol)
        today_str = dt.datetime.today().strftime('%Y-%m-%d')

        # If we got some data and we already checked for new stuff today 
        # then we have the latest stuff so return it
        if (result != None and
                result.last_check_date != None and
                result.last_check_date == today_str and
                result.financials != None):
            # We got a result and its not stale
            return json.loads(result.financials)

        # otherwise, this stuff mmight be stale
        elif result != None:
            # Call IEX and check what the latest report date is
            # (This is a free call to IEX)
            stock = myjinxstock.MyJinxStock(symbol)
            lfrd_dict = stock.get_latest_financial_report_date()
            latest_report_date = lfrd_dict['latestFinancialReportDate']

            # If the latest report date they have is newer than our reportDate
            # then we need to fetch the new stuff (so remvoe what we have)
            if (latest_report_date is None or
                    result.report_date is None or
                    latest_report_date > result.report_date):
                # Yup, there's new data. Remove our existing row.
                self._remove_financials(symbol)

            # Looks like what we have is the latest. Mark that we checked today
            # so we don't check anymore.
            else:
                # Nothing new. Just update the last_check_date
                return self._update_financials_last_check_date(symbol,
                                                               today_str)

        # If we're here, then we haven't returned anything yet. Must be time 
        # to get new result and return it.
        self._fetch_financials(symbol)
        result = self._get_financials_query(symbol)
        if (result != None
                and  result.financials != None):
            return json.loads(result.financials)
        else:
            return {}

    def _get_financials_query(self, symbol):
        """Get a single row in the financials table for the symbol if it exists

        Parameters
        ---------
        symbol :str
            The ticker symbol

        Returns
        -------
        Query: sqlalchemy.orm.query.Query
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
        """ Get data from IEX using jinx and write the results into our db.

        Parameters
        ---------
        synbol: str
            Ticker symbol
        """
        try:
            raw_dict = {'symbol': symbol}
            stock = myjinxstock.MyJinxStock(symbol)
            cf_dict = stock.get_cash_flow()
            if ('cashflow' in cf_dict and
                    len(cf_dict['cashflow']) > 0):
                raw_dict.update(cf_dict['cashflow'][0])
            else:
                logging.error('{} has no cash flow data'.format(symbol))

            is_dict = stock.get_income_statement()
            if ('income' in is_dict and
                    len(is_dict['income']) > 0):
                raw_dict.update(is_dict['income'][0])
            else:
                logging.error('{} has no income statement data'.format(symbol))

            bs_dict = stock.get_balance_sheet()
            if ('balancesheet' in bs_dict and
                    len(bs_dict['balancesheet']) > 0):
                raw_dict.update(bs_dict['balancesheet'][0])
            else:
                logging.error('{} has no balance sheet data'.format(symbol))

            company_dict = stock.get_company()
            if not company_dict:
                logging.error('{} has no company data'.format(symbol))
            else:
                raw_dict.update(company_dict)

            lfrd_dict = stock.get_latest_financial_report_date()
            if 'latestFinancialReportDate' in lfrd_dict:
                last_report_date = lfrd_dict['latestFinancialReportDate']
                raw_dict['latestFinancialReportDate'] = last_report_date
            else:
                last_report_date = None
                logging.error('{} has no latest financial reportdate'.
                              format(symbol))

        except Exception as e:
            logging.error('Error in _fetch_financials')
            logging.error('symbol:' + symbol)
            logging.error(e)
            return
        else:
            today = dt.datetime.today()
            last_check_date = today.strftime('%Y-%m-%d')

            session = db.session_factory()
            financial = Financials(symbol, json.dumps(raw_dict),
                                   last_report_date, last_check_date)
            session.add(financial)
            session.commit()
            session.close()

    def _remove_financials(self, symbol):
        session = db.session_factory()
        session.query(Financials).filter(Financials.symbol == symbol).delete()
        session.commit()
        session.close()

    def _update_financials_last_check_date(self, symbol, last_check_date):
        """Update the row in the financials table with a new last_check_date

        Paramaters
        ---------
        symbol: str
            The ticker symbol
        last_check_date: str
            The new that we last checked for financials

        Returns
        -------
        result: sqlalchemy query
            The updated financials row
        """

        session = db.session_factory()
        result = session.query(Financials).filter(
            Financials.symbol == symbol).one_or_none()
        result.last_check_date = last_check_date
        session.commit()
        session.close()
        if result == None:
            return None
        else:
            return result

def get_financials(symbol):
    return _qdb.get_financials(symbol)

_qdb = QuintanaDatabase()
