
class MarketData:

    def __init__(self, row_data):
        try:
            self.id = row_data['id']
        except IndexError:
            self.id = None

        self.ticker_code = row_data['ticker_code']
        self.fecha = row_data['fecha']
        self.apertura = row_data['apertura']
        self.maximo = row_data['maximo']
        self.minimo = row_data['minimo']
        self.cierre = row_data['cierre']
        self.volumen = row_data['volumen']


class Ticker:

    def __init__(self, row_data):
        try:
            self.id = row_data['id']
        except IndexError:
            self.id = None

        self.ticker_name = row_data['ticker_name']
        self.code = row_data['code']
        self.api = row_data['api']
        self.currency = row_data['currency']
