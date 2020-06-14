from flask import (
    Blueprint, render_template, request
)
from flaskr.auth import login_required
from flaskr.data import process_tickers
import logging
import flaskr.tickers_dao as t_dao


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
        tickers=tickers
    )


@bp.route('/submit_tickers', methods=['POST'])
@login_required
def submit_tickers():
    start_date = None
    end_date = None
    tickers_selected = []

    for k, v in request.form.items():
        if k == 'start':
            start_date = v
            continue

        if k == 'end':
            end_date = v
            continue

        tickers_selected.append(t_dao.get_ticker_byId(k))

    # LOG.debug(f"start_date: {start_date}")
    # LOG.debug(f"end_date: {end_date}")
    # LOG.debug(f"tickers_selected[0]: {tickers_selected[0]['code']}")
    # LOG.debug(f"tickers_selected[1]: {tickers_selected[1]['code']}")

    process_tickers(tickers_selected, start_date, end_date)

    return "pepe"
