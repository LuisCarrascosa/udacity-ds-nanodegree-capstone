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
  currency TEXT,
  last_date TEXT NOT NULL DEFAULT '2000-01-01',
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE models_data (
  id INTEGER PRIMARY KEY,
  pred_range INTEGER NOT NULL,
  window_len INTEGER NOT NULL,
  feature TEXT NOT NULL,
  fecha TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
); 

CREATE TABLE models_x_tickers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  models_id INTEGER NOT NULL,
  ticker_id INTEGER NOT NULL,
  ticker_type TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (ticker_id) REFERENCES tickers (id),
  FOREIGN KEY (models_id) REFERENCES models_data (id)
);

CREATE INDEX models_id ON models_x_tickers (models_id);

INSERT INTO tickers (code, ticker_name, currency) VALUES ("REP.MC", "REPSOL",  "EUR");
INSERT INTO tickers (code, ticker_name, currency) VALUES ("XOM", "Exxon Mobil Corp.",  "USD");
INSERT INTO tickers (code, ticker_name, currency) VALUES ("NDAQ", "Nasdaq Inc.",  "USD");
INSERT INTO tickers (code, ticker_name, currency) VALUES ("EEM", "Emerging Markets Ishares MSCI ETF",  "USD");
INSERT INTO tickers (code, ticker_name, currency) VALUES ("%5EDJI", "Dow Jones Industrial Average",  "USD");
INSERT INTO tickers (code, ticker_name, currency) VALUES ("ELE.MC", "Endesa, Sociedad Anonima",  "EUR");
INSERT INTO tickers (code, ticker_name, currency) VALUES ("TRE.MC", "Tecnicas Reunidas, S.A.",  "EUR");
INSERT INTO tickers (code, ticker_name, currency) VALUES ("ACX.MC", "Acerinox, S.A.",  "EUR");
INSERT INTO tickers (code, ticker_name, currency) VALUES ("SPY", "SPDR S&P 500 ETF",  "USD");
INSERT INTO tickers (code, ticker_name, currency) VALUES ("MTS.MC", "ArcelorMittal",  "EUR");
-- INSERT INTO tickers (code, ticker_name, currency) VALUES ("AMS.MC", "Amadeus IT Group, S.A.",  "EUR");
-- INSERT INTO tickers (code, ticker_name, currency) VALUES ("COL.MC", "Inmobiliaria Colonial, SOCIMI, S.A.",  "EUR");
INSERT INTO tickers (code, ticker_name, currency) VALUES ("IBE.MC", "Iberdrola, S.A.",  "EUR");
INSERT INTO tickers (code, ticker_name, currency) VALUES ("FER.MC", "Ferrovial, S.A.",  "EUR");
INSERT INTO tickers (code, ticker_name, currency) VALUES ("NTGY.MC", "Naturgy Energy Group, S.A.",  "EUR");
INSERT INTO tickers (code, ticker_name, currency) VALUES ("ITX.MC", "Industria de Diseno Textil, S.A.",  "EUR");
INSERT INTO tickers (code, ticker_name, currency) VALUES ("CLNX.MC", "Cellnex Telecom, S.A.",  "EUR");
INSERT INTO tickers (code, ticker_name, currency) VALUES ("VIS.MC", "Viscofan, S.A.",  "EUR");
INSERT INTO tickers (code, ticker_name, currency) VALUES ("GAZP.ME", "Public Joint Stock Company Gazprom",  "RUB");
INSERT INTO tickers (code, ticker_name, currency) VALUES ("ROSN.ME", "Public Joint Stock Company Rosneft Oil Company",  "RUB");
INSERT INTO tickers (code, ticker_name, currency) VALUES ("CVX", "Chevron Corporation",  "USD");
INSERT INTO tickers (code, ticker_name, currency) VALUES ("RDSA.AS", "Royal Dutch Shell Plc",  "EUR");
INSERT INTO tickers (code, ticker_name, currency) VALUES ("TEF.MC", "Telefónica, S.A.",  "EUR");
INSERT INTO tickers (code, ticker_name, currency) VALUES ("ACS.MC", "ACS, Actividades de Construccion y Servicios, S.A.",  "EUR");
INSERT INTO tickers (code, ticker_name, currency) VALUES ("0857.HK", "PetroChina Company Limited",  "HKD");
INSERT INTO tickers (code, ticker_name, currency) VALUES ("ENG.MC", "Enagas, S.A.",  "EUR");
INSERT INTO tickers (code, ticker_name, currency) VALUES ("AAPL", "Apple Inc.", "USD");
INSERT INTO tickers (code, ticker_name, currency) VALUES ("GOOG", "Alphabet Inc.", "USD");
INSERT INTO tickers (code, ticker_name, currency) VALUES ("MSFT", "Microsoft Corporation", "USD");

CREATE TABLE market_data (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ticker_id INTEGER NOT NULL,
  fecha TEXT NOT NULL, 
  apertura REAL NOT NULL,
  maximo REAL NOT NULL,
  minimo REAL NOT NULL,
  cierre REAL NOT NULL,
  cierre_ajustado REAL NOT NULL,
  volumen INTEGER ,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (ticker_id) REFERENCES tickers (id)
);

CREATE UNIQUE INDEX market_data_index ON market_data (ticker_id, fecha);

CREATE TABLE forex_data (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  currency_from TEXT NOT NULL,
  currency_to TEXT NOT NULL,
  fecha TEXT NOT NULL, 
  apertura REAL NOT NULL,
  maximo REAL NOT NULL,
  minimo REAL NOT NULL,
  cierre REAL NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
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