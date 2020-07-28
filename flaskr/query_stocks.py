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

bp = Blueprint('query_stocks', __name__, url_prefix='/query_stocks')
LOG = logging.getLogger(__name__)


@bp.route('/')
@login_required
def index():
    user_model_data, x_stocks, y_stocks = model_dao.load_model_data(
        int(session.get('user_id')))

    x_tickers = t_dao.get_tickers_inIds(x_stocks)
    y_tickers = t_dao.get_tickers_inIds(y_stocks)

    window_len = user_model_data['window_len']
    pred_range = user_model_data['pred_range']
    feature = user_model_data['feature']
    fecha = user_model_data['fecha']

    df = data_dao.load_dataframe_table(
        users_dao.select_user_byId(
            session.get('user_id')
        )['username'])

    last_i, r_scale, X_news, Y_news, LSTM_input = utils.getInput(
        df, y_tickers[0].code, window_len, pred_range, fecha)

    model = keras.models.load_model(f"models/{session.get('user_id')}")

    predicted_graph = painter.draw_prediction(
        model,
        last_i,
        pred_range,
        r_scale[y_tickers[0].code],
        X_news,
        Y_news,
        LSTM_input)

    return render_template(
        'query_stocks/query_stocks.html',
        x_tickers=x_tickers,
        y_tickers=y_tickers,
        window_len=window_len,
        pred_range=pred_range,
        feature=utils.get_feature_description(feature),
        last_fecha=fecha,
        predicted_graph=predicted_graph
    )
