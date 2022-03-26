from . import forum_blueprint
from flask import (
    flash, g, redirect, render_template, request, url_for
)
from sqlalchemy.exc import IntegrityError
from flaskr.auth import login_required, admin_required
from flaskr.db import db

@forum_blueprint.route('/forum/<int:forum_id>/topic/<int:topic_id>/create', methods=['GET'])
@login_required
def commentForm(forum_id, topic_id):
    getForum = 'SELECT * FROM forum WHERE id = (:forum_id)'
    forum = db.session.execute(getForum, { "forum_id": forum_id }).fetchone()
    
    getTopic = 'SELECT * FROM topic WHERE id = (:topic_id)'
    topic = db.session.execute(getTopic, { "topic_id": topic_id }).fetchone()
    
    return render_template('forum/create_comment.html', forum=forum, topic=topic)

@forum_blueprint.route('/forum/<int:forum_id>/topic/<int:topic_id>', methods=['POST'])
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

@forum_blueprint.route('/comment/<int:comment_id>', methods=['DELETE'])
@login_required
def deleteComment():
    pass

@forum_blueprint.route('/comment/<int:comment_id>', methods=['PATCH'])
@login_required
def editComment():
    pass
