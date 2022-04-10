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

@forum_blueprint.route('/comment/<int:comment_id>', methods=['GET'])
@login_required
def commentEditForm(comment_id):
    getFormData = '''
        SELECT
        forum.name AS forum_name,
        topic.title AS topic_title,
        comment.body AS comment_body
        FROM comment
        JOIN topic ON topic.id = comment.topic_id
        JOIN forum ON topic.forum_id = forum.id WHERE comment.id = :comment_id
    '''
    formData = db.session.execute(getFormData, { 'comment_id': comment_id }).fetchone()
    return render_template(
            'forum/edit_comment.html',
            forum_name=formData.forum_name,
            topic_title=formData.topic_title,
            comment_body=formData.comment_body,
            comment_id=comment_id) 

@forum_blueprint.route('/forum/<int:forum_id>/topic/<int:topic_id>', methods=['POST'])
@login_required
def createComment(forum_id, topic_id):
    comment_body = request.form['body']
    insertComment = 'INSERT INTO comment (body, account_id, topic_id) values (:body, :account, :topic)'
    values = { 'body': comment_body, 'account': g.user.id, 'topic': topic_id}
    try:
        db.session.execute(insertComment, values)
        db.session.commit()
    except IntegrityError:
        flash('Error creating new comment')
    return redirect(url_for("forum.topic", forum_id=forum_id, topic_id=topic_id))

@forum_blueprint.route('/comment/<int:comment_id>', methods=['DELETE'])
@login_required
def deleteComment():
    pass

@forum_blueprint.route('/comment/<int:comment_id>', methods=['POST'])
@login_required
def editComment(comment_id):
    getTopicData = '''
        SELECT forum_id, topic_id 
        FROM comment
        JOIN topic ON comment.topic_id = topic.id
        WHERE comment.id = :comment_id
    '''
    topicData = db.session.execute(getTopicData, { 'comment_id': comment_id }).fetchone()

    getCommentAccount = 'SELECT account_id as id FROM comment WHERE comment.id = :comment_id'
    commentAccount = db.session.execute(getCommentAccount, {'comment_id': comment_id}).fetchone()

    if (g.user.id is not commentAccount.id):
        flash('Thats not your comment')
        return redirect(url_for("forum.topic", forum_id=topicData.forum_id, topic_id=topicData.topic_id))


    comment_body = request.form['body']
    updateComment = 'UPDATE comment SET body = :comment_body WHERE id = :comment_id'
    values = { 'comment_body': comment_body, 'comment_id': comment_id}

    try:
        db.session.execute(updateComment, values)
        db.session.commit()
    except IntegrityError:
        flash('Error editing comment')

    return redirect(url_for("forum.topic", forum_id=topicData.forum_id, topic_id=topicData.topic_id))

