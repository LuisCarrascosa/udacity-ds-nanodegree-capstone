from flask import (
    Blueprint,
    render_template,
    request, session, redirect, url_for
)
from flaskr.auth import login_required
from datetime import date
import flaskr.utils as utils
import flaskr.market_data_dao as data_dao
import flaskr.finantial_utils as fin_utils
import flaskr.tickers_dao as t_dao
import flaskr.painter as painter
import datetime
import logging


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
        # start_date=date.today() - timedelta(days=30),
        start_date=date(2010, 1, 1),
        end_date=date.today(),
        today=date.today(),
        min_date=date(2010, 1, 1)
    )


@bp.route('/submit_tickers', methods=['POST'])
@login_required
def submit_tickers():
    form_data = utils.get_data_select_data_form(request.form.items())
    form_data['tickers_selected'].insert(0, form_data['stock_select'])

    start_date = form_data['start_date']

    df = data_dao.get_data_on_feature(
        form_data['feature'],
        form_data['tickers_selected'],
        start_date,
        form_data['end_date']
    )

    ncols = 1
    nrows = len(df.columns)

    df.fillna(method='pad', axis=0, inplace=True)

    data_graph = painter.drawFeatures_byDict(
        df, nrows, ncols,
        tickers=form_data['tickers_selected'],
        f_ini=start_date,
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


@bp.route('/training', methods=['POST'])
@login_required
def training():
    form_data = utils.get_data_select_data_form(request.form.items())
    form_data['tickers_selected'].insert(0, form_data['stock_select'])

    start_date = form_data['start_date']
    fecha_ini = start_date - datetime.timedelta(days=60)

    df = data_dao.get_data_on_feature(
        form_data['feature'],
        form_data['tickers_selected'],
        fecha_ini,
        form_data['end_date']
    )

    df.fillna(method='pad', axis=0, inplace=True)
    df = fin_utils.get_technical_indicators(df, form_data['stock_select'].code)

    utils.save_session(session, form_data, df[df.index >= start_date])

    return redirect(url_for("training.index"))
