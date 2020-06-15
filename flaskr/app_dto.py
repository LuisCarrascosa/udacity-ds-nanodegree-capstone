
class MarketData:

    def __init__(self, data):
        try:
            self.id = data['id']
        except KeyError:
            self.id = None

        self.ticker_code = data['ticker_code']
        self.fecha = data['fecha']
        self.apertura = data['apertura']
        self.maximo = data['maximo']
        self.minimo = data['minimo']
        self.cierre = data['cierre']
        self.volumen = data['volumen']


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
