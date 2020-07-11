class Ticker:

    def __init__(self, data):
        try:
            self.id = data['id']
        except KeyError:
            self.id = None

        self.ticker_name = data['ticker_name']
        self.code = data['code']
        self.currency = data['currency']
        self.df = None

    def __eq__(self, other):
        if not other:
            return False

        return self.id == other.id

    def __ne__(self, other):
        return not self == other


data = {}
data['id'] = 1
data['ticker_name'] = "Pepe"
data['code'] = "001"
data['currency'] = "EUR"

ticker1 = Ticker(data)

data['id'] = 5
data['ticker_name'] = "Pepe"
data['code'] = "001"
data['currency'] = "EUR"
ticker2 = Ticker(data)

data['id'] = 2
data['ticker_name'] = "Alberto"
data['code'] = "002"
data['currency'] = "EUR"

ticker3 = Ticker(data)

buffer = [ticker1, ticker2, ticker3]

print(buffer)
buffer.remove(ticker2)
print(buffer)
