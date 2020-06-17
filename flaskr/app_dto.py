
class Ticker:

    def __init__(self, data):
        try:
            self.id = data['id']
        except KeyError:
            self.id = None

        self.ticker_name = data['ticker_name']
        self.code = data['code']
        self.api = data['api']
        self.currency = data['currency']
