from flask import (
    Blueprint, render_template, request
)

from flaskr.db import db


bp = Blueprint('search', __name__, url_prefix='/search')
@bp.route('/', methods=(['GET']))
def search():
    query = request.args.get('q')
    if query is None:
        redirect(url_for('index'))
    getComments = "SELECT * FROM comment WHERE lower(body) LIKE lower(concat('%', :query, '%'))"
    comments = db.session.execute(getComments, { 'query': query }).fetchall()
    return render_template('search.html', comments=comments)
    

