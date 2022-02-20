from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import db

bp = Blueprint('forum', __name__)

@bp.route('/')
def index():
     getForums = 'SELECT * FROM forum'
     forums = db.session.execute(getForums).fetchall()
     return render_template('forum/index.html', forums=forums)

@bp.route('/forum/<int:forum_id>')
def forum(forum_id):
     getForum = 'SELECT * FROM forum WHERE id = (:forum_id)'
     forum = db.session.execute(getForum, { "forum_id": forum_id }).fetchone()

     getTopics = 'SELECT * FROM topic WHERE forum_id = (:forum_id)'
     topics = db.session.execute(getTopics, { "forum_id": forum_id }).fetchall()

     return render_template('forum/forum.html', title=forum.name, topics=topics)

@bp.route('/forum/<int:forum_id>/topic/<int:topic_id>')
def topic(forum_id):
     pass
