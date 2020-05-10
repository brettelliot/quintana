from jinx.stock import Stock

class MyJinxStock(Stock):
    """
    MyJinxStock is a helpful subclass that allows me to patch any problems
    in the jinx Stock class.
    """

    def __init__(self, symbol=None, **kwargs):
        super(MyJinxStock, self).__init__(symbol, **kwargs)

    def get_latest_financial_report_date2(self):
        result_dict = super().get_latest_financial_report_date()
        last_report_date = result_dict['latestFinancialReportDate']
        result_dict['latestFinancialReportDate'] = \
                last_report_date.replace('"',"")
        return result_dict

