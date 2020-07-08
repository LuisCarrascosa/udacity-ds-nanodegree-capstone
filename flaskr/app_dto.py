
class Ticker:

    def __init__(self, data):
        try:
            self.id = data['id']
        except KeyError:
            self.id = None

        self.ticker_name = data['ticker_name']
        self.code = data['code']
        self.currency = data['currency']
        self.last_date = data['last_date']
        self.df = None

    def set_data(self, df):
        self.df = df
