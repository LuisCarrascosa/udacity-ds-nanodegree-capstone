DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS market_data;
DROP TABLE IF EXISTS forex_data;
DROP TABLE IF EXISTS exchanges;
DROP TABLE IF EXISTS tickers;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE tickers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  code TEXT NOT NULL,
  ticker_name TEXT NOT NULL,
  api TEXT NOT NULL,
  currency TEXT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO tickers (code, ticker_name, api, currency) VALUES ("REP.MC", "REPSOL", "alphavantage_daily", "EUR");
INSERT INTO tickers (code, ticker_name, api, currency) VALUES ("XOM", "Exxon Mobil Corp.", "alphavantage_daily", "USD");
INSERT INTO tickers (code, ticker_name, api, currency) VALUES ("NDAQ", "Nasdaq Inc.", "alphavantage_daily", "USD");
INSERT INTO tickers (code, ticker_name, api, currency) VALUES ("EEM", "Emerging Markets Ishares MSCI ETF", "alphavantage_daily", "USD");
INSERT INTO tickers (code, ticker_name, api, currency) VALUES ("DJI", "DOW JONES", "alphavantage_daily", NULL);
INSERT INTO tickers (code, ticker_name, api, currency) VALUES ("ELE.MC", "Endesa, Sociedad Anonima", "alphavantage_daily", "EUR");
INSERT INTO tickers (code, ticker_name, api, currency) VALUES ("TRE.MDR", "Tecnicas Reunidas, S.A.", "alphavantage_daily", "EUR");
INSERT INTO tickers (code, ticker_name, api, currency) VALUES ("ACX.MC", "Acerinox, S.A.", "alphavantage_daily", "EUR");
INSERT INTO tickers (code, ticker_name, api, currency) VALUES ("SPY", "SPDR S&P 500 ETF", "alphavantage_daily", "USD");
INSERT INTO tickers (code, ticker_name, api, currency) VALUES ("MTS.MC", "ArcelorMittal", "alphavantage_daily", "EUR");
INSERT INTO tickers (code, ticker_name, api, currency) VALUES ("AMS.MC", "Amadeus IT Group, S.A.", "alphavantage_daily", "EUR");
INSERT INTO tickers (code, ticker_name, api, currency) VALUES ("COL.MC", "Inmobiliaria Colonial, SOCIMI, S.A.", "alphavantage_daily", "EUR");
INSERT INTO tickers (code, ticker_name, api, currency) VALUES ("IBE.MC", "Iberdrola, S.A.", "alphavantage_daily", "EUR");
INSERT INTO tickers (code, ticker_name, api, currency) VALUES ("FER.MC", "Ferrovial, S.A.", "alphavantage_daily", "EUR");
INSERT INTO tickers (code, ticker_name, api, currency) VALUES ("NTGY.MC", "Naturgy Energy Group, S.A.", "alphavantage_daily", "EUR");
INSERT INTO tickers (code, ticker_name, api, currency) VALUES ("ITX.MC", "Industria de Diseno Textil, S.A.", "alphavantage_daily", "EUR");
INSERT INTO tickers (code, ticker_name, api, currency) VALUES ("CLNX.MC", "Cellnex Telecom, S.A.", "alphavantage_daily", "EUR");
INSERT INTO tickers (code, ticker_name, api, currency) VALUES ("VIS.MC", "Viscofan, S.A.", "alphavantage_daily", "EUR");
INSERT INTO tickers (code, ticker_name, api, currency) VALUES ("GAZP.ME", "Public Joint Stock Company Gazprom", "alphavantage_daily", "RUB");
INSERT INTO tickers (code, ticker_name, api, currency) VALUES ("ROSN.ME", "Public Joint Stock Company Rosneft Oil Company", "alphavantage_daily", "RUB");
INSERT INTO tickers (code, ticker_name, api, currency) VALUES ("CVX", "Chevron Corporation", "alphavantage_daily", "USD");
INSERT INTO tickers (code, ticker_name, api, currency) VALUES ("RDSA.AS", "Royal Dutch Shell Plc", "alphavantage_daily", "EUR");
INSERT INTO tickers (code, ticker_name, api, currency) VALUES ("TEF.MC", "Telefónica, S.A.", "alphavantage_daily", "EUR");
INSERT INTO tickers (code, ticker_name, api, currency) VALUES ("ACS.MC", "ACS, Actividades de Construccion y Servicios, S.A.", "worldtradingdata", "EUR");
INSERT INTO tickers (code, ticker_name, api, currency) VALUES ("0857.HK", "PetroChina Company Limited", "worldtradingdata", "HKD");
INSERT INTO tickers (code, ticker_name, api, currency) VALUES ("ENG.MC", "Enagas, S.A.", "worldtradingdata", "EUR");

-- INSERT INTO datetime_int (d1) VALUES(strftime("%s","now"););
-- SELECT datetime(d1,"unixepoch"); FROM datetime_int;
CREATE TABLE market_data (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ticker_code TEXT NOT NULL,
  fecha TEXT NOT NULL, 
  apertura REAL NOT NULL,
  maximo REAL NOT NULL,
  minimo REAL NOT NULL,
  cierre REAL NOT NULL,
  volumen INTEGER ,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (ticker_code) REFERENCES tickers (code)
);

CREATE INDEX ticker_code ON market_data (ticker_code);

CREATE TABLE forex_data (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  currency_from TEXT NOT NULL,
  currency_to TEXT NOT NULL,
  fecha TEXT NOT NULL, 
  apertura REAL NOT NULL,
  maximo REAL NOT NULL,
  minimo REAL NOT NULL,
  cierre REAL NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (fecha) REFERENCES market_data (fecha)
);

CREATE INDEX currency_from ON forex_data (currency_from);

CREATE TABLE exchanges (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  code TEXT NOT NULL,
  currency_from TEXT NOT NULL,
  currency_to TEXT NOT NULL,
  api TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (currency_from, currency_to) REFERENCES forex_data (currency_from, currency_to)
);

INSERT INTO exchanges (code, currency_from, currency_to, api) VALUES ("FOREX_USD_EUR", "USD", "EUR", "alphavantage_fx_daily");
INSERT INTO exchanges (code, currency_from, currency_to, api) VALUES ("FOREX_RUB_EUR", "RUB", "EUR", "alphavantage_fx_daily");
INSERT INTO exchanges (code, currency_from, currency_to, api) VALUES ("FOREX_HKD_EUR", "HKD", "EUR", "alphavantage_fx_daily");
INSERT INTO exchanges (code, currency_from, currency_to, api) VALUES ("FOREX_BRL_EUR", "BRL", "EUR", "alphavantage_fx_daily");