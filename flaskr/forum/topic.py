from . import forum_blueprint
from flask import (
    flash, g, redirect, render_template, request, url_for
)
from sqlalchemy.exc import IntegrityError
from flaskr.auth import login_required
from flaskr.db import db

@forum_blueprint.route('/forum/<int:forum_id>/topic/<int:topic_id>', methods=['GET'])
def topic(forum_id, topic_id):
    getForum = 'SELECT * FROM forum WHERE id = (:forum_id)'
    forum = db.session.execute(getForum, { "forum_id": forum_id }).fetchone()
    
    getTopic = 'SELECT * FROM topic WHERE id = (:topic_id)'
    topic = db.session.execute(getTopic, { "topic_id": topic_id }).fetchone()

    getComments = '''
        SELECT account.username, comment.*
        FROM comment JOIN account on account.id = comment.account_id
        WHERE comment.topic_id = :topic_id;
    '''
    values = { 'topic_id': topic_id }
    comments = db.session.execute(getComments, values).fetchall()

    return render_template('forum/topic.html', forum=forum, topic=topic, comments=comments)

@forum_blueprint.route('/forum/<int:forum_id>/create', methods=['GET'])
@login_required
def topicForm(forum_id):
    getForum = 'SELECT * FROM forum WHERE id = (:forum_id)'
    forum = db.session.execute(getForum, { "forum_id": forum_id }).fetchone()
    return render_template('forum/create_topic.html', forum=forum)


@forum_blueprint.route('/forum/<int:forum_id>', methods=['POST'])
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

@forum_blueprint.route('/topic/<int:topic_id>', methods=['DELETE'])
@login_required
def deleteTopic():
    pass
    

