from flask import (
    Blueprint, render_template, request
)
from flaskr.auth import login_required
from datetime import date, timedelta
from flaskr.market_data_dao import get_data_on_feature
import flaskr.utils as utils
import flaskr.finantial_utils as fin_utils
import logging


bp = Blueprint('training', __name__, url_prefix='/training')
LOG = logging.getLogger(__name__)


# A training interface that accepts a data range
# (start_date, end_date) and a list of ticker symbols (e.g. GOOG, AAPL),
# and builds a model of stock behavior. Your code should read the
# desired historical prices from the data source of your choice.
@bp.route('', methods=['POST'])
@login_required
def index():
    form_data = utils.get_data_select_data_form(request.form.items())
    form_data['tickers_selected'].insert(0, form_data['stock_select'])

    df = get_data_on_feature(
        form_data['feature'],
        form_data['tickers_selected'],
        form_data['start_date'],
        form_data['end_date']
    )

    # print(df.tail(10))
    df.fillna(method='pad', axis=0, inplace=True)
    # print(df.shape)

    df = fin_utils.get_technical_indicators(df, form_data['stock_select'].code)

    # print(df.shape)
    # print(df.tail(10))

    return render_template(
        'training/training.html',
    )
