from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError

from flaskr.auth import login_required, admin_required
from flaskr.db import db

bp = Blueprint('forum', __name__)

@bp.route('/')
def index():
    if g.user is not None:
        getUserForums = '''
            SELECT forum.* FROM forum
            WHERE NOT forum.private OR forum.password IS NOT NULL
            UNION
            SELECT forum.* FROM forum JOIN private_forum_account ON private_forum_account.forum_id = forum.id
            WHERE private_forum_account.account_id = :account_id;

        '''
        if g.user.is_admin:
            getUserForums = 'SELECT * FROM forum'
        forums = db.session.execute(getUserForums, { 'account_id': g.user.id}).fetchall()
    else:
        getPublicForums = 'SELECT * FROM forum WHERE NOT private'
        forums = db.session.execute(getPublicForums).fetchall()

    return render_template('forum/index.html', forums=forums)

@bp.route('/forum/<int:forum_id>', methods=['GET'])
def forum(forum_id):
    getForum = 'SELECT * FROM forum WHERE id = (:forum_id)'
    forum = db.session.execute(getForum, { "forum_id": forum_id }).fetchone()

    getTopics = 'SELECT * FROM topic WHERE forum_id = (:forum_id)'
    topics = db.session.execute(getTopics, { "forum_id": forum_id }).fetchall()

    return render_template('forum/forum.html', forum=forum, topics=topics)

@bp.route('/forum/create', methods=['GET'])
@login_required
def forumForm():
    return render_template('forum/create_forum.html')

@bp.route('/forum', methods=['POST'])
@admin_required
@login_required
def createForum():
    forum_name = request.form['name']
    forum_description = request.form['description']
    forum_password = request.form['password']
    # A html checkbox evaluates to 'on' when checked i.e when forum is private
    forum_is_private = request.form.get('private') == 'on'
      
    error = None
    insertForum = None
    insertPrivateForumAccount = None

    if forum_password and not forum_is_private:
        error = 'Public forums cannot be password protected'

    if forum_password:
        forum_password = generate_password_hash(forum_password)
        insertForum = 'INSERT INTO forum (name, description, private, password, creator_account) VALUES (:name, :description, :private, :password, :creator_account) RETURNING *'
        values = { 'name': forum_name, 'description': forum_description, 'private': forum_is_private, 'password': forum_password, 'creator_account': g.user.id }
    else:
        insertForum = 'INSERT INTO forum (name, description, private, creator_account) VALUES (:name, :description, :private, :creator_account) RETURNING *'
        values = { 'name': forum_name, 'description': forum_description, 'private': forum_is_private, 'creator_account': g.user.id}

    if forum_is_private:
        insertPrivateForumAccount = 'INSERT INTO private_forum_account (account_id, forum_id) VALUES (:account_id, :forum_id)'

    if error is not None:
        flash(error)
        return redirect(url_for("forum.forumForm"))

    try:
        result = db.session.execute(insertForum, values).fetchone()
        if (insertPrivateForumAccount is not None):
            db.session.execute(insertPrivateForumAccount, { 'account_id': g.user.id, 'forum_id': result.id })
        db.session.commit()
        return redirect(url_for("forum.index"))
    except IntegrityError:
        flash('Error creating new forum')
        return redirect(url_for("forum.forumForm"))

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
        return redirect(url_for("forum.topicForm", forum_id=forum_id))

    
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
    

