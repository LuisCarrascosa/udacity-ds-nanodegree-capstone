from flask import (
    Blueprint, redirect, render_template, url_for, session
)
from flaskr.auth import login_required
import logging

bp = Blueprint('main', __name__)
LOG = logging.getLogger(__name__)


@bp.route('/')
@login_required
def main():
    for session_key in session:
        print(f"SESSION: {session_key} / {session[session_key]}")

    return render_template(
        'main/main.html',
        opciones=[{
            "code": "data_aquisition",
            "description": "Data aquisition"
        }, {
            "code": "stocks_selection",
            "description": "Training"
        }, {
            "code": "query_stocks",
            "description": "Query stocks"
        }]
    )


@bp.route('/menu_select/<id_option>', methods=['GET'])
@login_required
def menu_select(id_option):
    # LOG.debug(f"id_option: {id_option}")
    return redirect(url_for(id_option))
