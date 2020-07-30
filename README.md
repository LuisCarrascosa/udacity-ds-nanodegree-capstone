# udacity-ds-nanodegree-capstone
## luis.carrascosa.next@bbva.com
### Project Overview
In this project we want to provide a web interface that allows:
- Acquisition of data on company quotes, funds or stock exchange indexes
- Training of a LSTM model
- Predicting product quotes

Flask is used on a SQLite database. Bootstrap is used for the layout.

Stocks prices are obtained from [yahoo finance](https://es.finance.yahoo.com/), downloading the csvs and storing them in the database

### Project Statement
The problem to be solved is the prediction of the prices of a stock. LSTM will be used for this purpose, taking as inputs:
- past prices of the stock
- technical value indicators of the stock
- past prices of stocks related to the target

After the training of the model, the predictions will be shown against the last stock prices. In case more recent data have been obtained since the model was trained, they will also be shown to compare every day how reality evolves against the prediction.

It is expected that, although the predictions are not completely accurate, if we are able to anticipate trends that advise purchases or sales of shares of the target stock market value.

As a stock portfolio cannot have a single value, it is allowed that there are several models with different target values with their corresponding related values.

### Metrics
The MAE (Mean Absolute Error) metric is used during the training of the model to decide whether to keep or re-training the model by changing some parameter of the model (neurons, epochs, etc)


