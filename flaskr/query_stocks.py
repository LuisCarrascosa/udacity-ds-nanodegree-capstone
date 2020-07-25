from flask import (
    Blueprint, render_template, request, session, jsonify
)
from flaskr.auth import login_required
from tensorflow import keras
import flaskr.model_data_dao as model_dao
import flaskr.tickers_dao as t_dao
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

    # model = keras.models.load_model(f"models/{session.get('user_id')}")

    return render_template(
        'query_stocks/query_stocks.html',
        x_tickers=x_tickers,
        y_tickers=y_tickers,
        window_len=window_len,
        pred_range=pred_range,
        feature=feature,
        last_fecha=fecha
    )


# @bp.route('/submit_tickers', methods=['POST'])
# @login_required
# def submit_tickers():
