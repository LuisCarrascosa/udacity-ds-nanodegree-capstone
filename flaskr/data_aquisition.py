from flask import (
    Blueprint, redirect, url_for
)
from flaskr.auth import login_required
import flaskr.market_data_dao as data_dao
import flaskr.yahoo_downloader as api_data
import logging
import flaskr.tickers_dao as t_dao


bp = Blueprint('data_aquisition', __name__, url_prefix='/data_aquisition')
LOG = logging.getLogger(__name__)


@bp.route('/')
@login_required
def index():
    tickers = api_data.get_data(t_dao.get_outdated())
    data_dao.save_data(tickers)
    return redirect(url_for('main'))
