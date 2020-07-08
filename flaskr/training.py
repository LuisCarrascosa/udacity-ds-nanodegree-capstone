from flask import (
    Blueprint, render_template, request
)
from flaskr.auth import login_required
from flaskr.market_data_dao import get_data_on_feature
from datetime import date, timedelta
import logging
import datetime
import flaskr.tickers_dao as t_dao
import flaskr.painter as painter


bp = Blueprint('training', __name__, url_prefix='/training')
LOG = logging.getLogger(__name__)


# A training interface that accepts a data range
# (start_date, end_date) and a list of ticker symbols (e.g. GOOG, AAPL),
# and builds a model of stock behavior. Your code should read the
# desired historical prices from the data source of your choice.
@bp.route('/')
@login_required
def index():
    tickers = t_dao.selectAll()

    return render_template(
        'training/training.html',
        tickers=tickers,
        today_30d=date.today() - timedelta(days=30),
        today=date.today()
    )


@bp.route('/submit_tickers', methods=['POST'])
@login_required
def submit_tickers():
    # start_date = None
    # end_date = None
    tickers_selected = []

    for k, v in request.form.items():
        print(f'{k}, {v}')

        if k == 'start':
            start_date = datetime.datetime.strptime(v, "%Y-%m-%d")
            continue

        if k == 'end':
            end_date = datetime.datetime.strptime(v, "%Y-%m-%d")
            continue

        if k == 'feature_select':
            feature = v
            continue

        tickers_selected.append(t_dao.get_ticker_byId(k))

    df = get_data_on_feature(feature, tickers_selected, start_date, end_date)
    print(df.tail())

    num_tickers = len(df.columns)
    if num_tickers <= 2:
        nrows = 1
        ncols = num_tickers
    else:
        ncols = 2
        nrows = int(num_tickers/ncols) + 1*(num_tickers % ncols)

    df.fillna(method='pad', axis=0, inplace=True)
    # print(df.tail())

    data_graph = painter.drawFeatures_byDict(
        df, nrows, ncols, f_ini=start_date, f_fin=end_date)

    # with open("grafica.png", "w") as fo:
    #     fo.write(data_graph)

    return render_template(
        'training/training.html',
        data_graph=data_graph
    )
