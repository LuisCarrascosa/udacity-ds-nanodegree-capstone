from flask import (
    Blueprint, render_template, session
)
from flaskr.auth import login_required
from tensorflow import keras
import flaskr.model_data_dao as model_dao
import flaskr.tickers_dao as t_dao
import flaskr.painter as painter
import flaskr.utils as utils
import flaskr.users_dao as users_dao
import flaskr.market_data_dao as data_dao
import logging
import numpy as np
import datetime
import pandas as pd

bp = Blueprint('query_stocks', __name__, url_prefix='/query_stocks')
LOG = logging.getLogger(__name__)


@bp.route('/')
@login_required
def index():
    user_model_data, x_stocks, y_stocks = model_dao.load_model_data(
        int(session.get('user_id')))

    x_tickers = [ticker for ticker in t_dao.get_tickers_inIds(x_stocks)]
    y_tickers = [ticker for ticker in t_dao.get_tickers_inIds(y_stocks)]

    stock = y_tickers[0].code
    stock_id = y_stocks[0]
    stock_name = y_tickers[0].ticker_name

    window_len = int(user_model_data['window_len'])
    pred_range = int(user_model_data['pred_range'])
    feature = user_model_data['feature']
    fecha = datetime.datetime.strptime(user_model_data['fecha'], "%Y-%m-%d")

    df = data_dao.load_dataframe_table(
        users_dao.select_user_byId(
            session.get('user_id')
        )['username'])

# fecha, {feature}
    mk_data = data_dao.get_market_data(stock_id, fecha, feature=feature)

    i_predict = df[df['Fecha'] == fecha].index[0]
    # print(i_predict)

    df_frame = df.iloc[[x for x in range(i_predict-window_len+1, i_predict+1)]]
    df_frame.index = pd.RangeIndex(start=0, stop=len(df_frame), step=1)

    x_df = df_frame.drop(['Fecha', stock], axis=1, inplace=False)
    y_df = df_frame[stock]
    # print(f"y_df: {y_df}")

    for col in list(x_df):
        x_df.loc[:, col] = x_df[col]/x_df[col].iloc[0] - 1

    LSTM_input = []
    LSTM_input.append(np.array(x_df))
    LSTM_input = np.array(LSTM_input)

    model = keras.models.load_model(f"models/{session.get('user_id')}")
    prediction = (model.predict(LSTM_input) + 1) * y_df[0]

    predicted_graph = painter.draw_prediction(
        model, pred_range, stock_name,
        mk_data, feature,
        fecha, y_df, prediction)

    return render_template(
        'query_stocks/query_stocks.html',
        x_tickers=x_tickers,
        y_tickers=y_tickers,
        window_len=window_len,
        pred_range=pred_range,
        feature=utils.get_feature_description(feature),
        last_fecha=fecha.date(),
        predicted_graph=predicted_graph
    )
