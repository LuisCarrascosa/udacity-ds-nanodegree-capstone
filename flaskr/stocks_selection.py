from flask import (
    Blueprint, render_template, request
)
from flaskr.auth import login_required
from flaskr.market_data_dao import get_data_on_feature
import flaskr.utils as utils
from datetime import date, timedelta
import logging
import flaskr.tickers_dao as t_dao
import flaskr.painter as painter


bp = Blueprint('stocks_selection', __name__, url_prefix='/stocks_selection')
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
        'stocks_selection/stocks_selection.html',
        tickers=tickers,
        start_date=date.today() - timedelta(days=30),
        end_date=date.today(),
        today=date.today()
    )


@bp.route('/submit_tickers', methods=['POST'])
@login_required
def submit_tickers():
    form_data = utils.get_data_select_data_form(request.form.items())
    form_data['tickers_selected'].insert(0, form_data['stock_select'])

    df = get_data_on_feature(
        form_data['feature'],
        form_data['tickers_selected'],
        form_data['start_date'],
        form_data['end_date']
    )

    ncols = 1
    nrows = len(df.columns)

    df.fillna(method='pad', axis=0, inplace=True)

    data_graph = painter.drawFeatures_byDict(
        df, nrows, ncols,
        f_ini=form_data['start_date'],
        f_fin=form_data['end_date']
    )

    form_data['tickers_selected'].remove(form_data['stock_select'])

    return render_template(
        'stocks_selection/stocks_selection.html',
        data_graph=data_graph,
        tickers=t_dao.selectAll(),
        start_date=form_data['start_date'].date(),
        end_date=form_data['end_date'].date(),
        today=date.today(),
        tickers_selected=form_data['tickers_selected'],
        feature=form_data['feature'],
        stock=int(form_data['stock_select'].id)
    )
