from flask import (
    Blueprint, redirect, render_template, url_for
)

from flaskr.auth import login_required
import logging

bp = Blueprint('main', __name__)
LOG = logging.getLogger(__name__)


@bp.route('/')
@login_required
def main():
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

# @bp.route('/create', methods=('GET', 'POST'))
# @login_required
# def create():
#     if request.method == 'POST':
#         title = request.form['title']
#         body = request.form['body']
#         error = None

#         if not title:
#             error = 'Title is required.'

#         if error is not None:
#             flash(error)
#         else:
#             db = get_db()
#             db.execute(
#                 'INSERT INTO post (title, body, author_id)'
#                 ' VALUES (?, ?, ?)',
#                 (title, body, g.user['id'])
#             )
#             db.commit()
#             return redirect(url_for('blog.index'))

#     return render_template('blog/create.html')
