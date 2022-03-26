from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from sqlalchemy.exc import IntegrityError

from flaskr.auth import login_required
from flaskr.db import db

bp = Blueprint('forum', __name__)

@bp.route('/')
def index():
    getForums = 'SELECT * FROM forum'
    forums = db.session.execute(getForums).fetchall()
    return render_template('forum/index.html', forums=forums)


@bp.route('/forum/<int:forum_id>', methods=['GET'])
def forum(forum_id):
    getForum = 'SELECT * FROM forum WHERE id = (:forum_id)'
    forum = db.session.execute(getForum, { "forum_id": forum_id }).fetchone()

    getTopics = 'SELECT * FROM topic WHERE forum_id = (:forum_id)'
    topics = db.session.execute(getTopics, { "forum_id": forum_id }).fetchall()

    return render_template('forum/forum.html', forum=forum, topics=topics)

@bp.route('/forum/<int:forum_id>', methods=['POST'])
@login_required
def createTopic(forum_id):
    topic_title = request.form['title']
    topic_body = request.form['body']
    insertTopic = 'INSERT INTO topic (title, body, account_id, forum_id) values (:title, :body, :account, :forum)'
    values = { 'title': topic_title, 'body': topic_body, 'account': g.user.id, 'forum': forum_id }
    try:
        db.session.execute(insertTopic, values)
        db.session.commit()
        return redirect(url_for("forum.forum", forum_id=forum_id))
    except IntegrityError:
        flash('Error creating new topic')
    
@bp.route('/forum/<int:forum_id>/create', methods=['GET'])
@login_required
def topicForm(forum_id):
    getForum = 'SELECT * FROM forum WHERE id = (:forum_id)'
    forum = db.session.execute(getForum, { "forum_id": forum_id }).fetchone()
    return render_template('forum/create_topic.html', forum=forum)

@bp.route('/forum/<int:forum_id>/topic/<int:topic_id>', methods=['GET'])
def topic(forum_id, topic_id):
    getForum = 'SELECT * FROM forum WHERE id = (:forum_id)'
    forum = db.session.execute(getForum, { "forum_id": forum_id }).fetchone()
    
    getTopic = 'SELECT * FROM topic WHERE id = (:topic_id)'
    topic = db.session.execute(getTopic, { "topic_id": topic_id }).fetchone()

    getComments = '''
        SELECT account.username, comment.body
        FROM comment JOIN account on account.id = comment.account_id
        WHERE comment.topic_id = :topic_id;
    '''
    values = { 'topic_id': topic_id }
    comments = db.session.execute(getComments, values).fetchall()

    return render_template('forum/topic.html', forum=forum, topic=topic, comments=comments)

@bp.route('/forum/<int:forum_id>/topic/<int:topic_id>/create', methods=['GET'])
@login_required
def commentForm(forum_id, topic_id):
    getForum = 'SELECT * FROM forum WHERE id = (:forum_id)'
    forum = db.session.execute(getForum, { "forum_id": forum_id }).fetchone()
    
    getTopic = 'SELECT * FROM topic WHERE id = (:topic_id)'
    topic = db.session.execute(getTopic, { "topic_id": topic_id }).fetchone()
    
    return render_template('forum/create_comment.html', forum=forum, topic=topic)

@bp.route('/forum/<int:forum_id>/topic/<int:topic_id>', methods=['POST'])
@login_required
def createComment(forum_id, topic_id):
    comment_body = request.form['body']
    insertComment = 'INSERT INTO comment (body, account_id, topic_id) values (:body, :account, :topic)'
    values = { 'body': comment_body, 'account': g.user.id, 'topic': topic_id}
    try:
        db.session.execute(insertComment, values)
        db.session.commit()
        return redirect(url_for("forum.topic", forum_id=forum_id, topic_id=topic_id))
    except IntegrityError:
        flash('Error creating new comment')
    

