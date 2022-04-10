from . import forum_blueprint
from flask import (
    flash, g, redirect, render_template, request, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError
from flaskr.auth import login_required, admin_required
from flaskr.db import db

@forum_blueprint.route('/')
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

@forum_blueprint.route('/forum/<int:forum_id>', methods=['GET'])
def forum(forum_id):
    getForum = 'SELECT * FROM forum WHERE id = (:forum_id)'
    forum = db.session.execute(getForum, { "forum_id": forum_id }).fetchone()
    error = None

    is_forum_member = True
    if (forum.private):
        is_forum_member_query = '''
            SELECT EXISTS(
            SELECT * FROM private_forum_account 
            WHERE account_id = :account_id AND forum_id = :forum_id
            ) AS is_member
        ''' 
        values = { 'account_id': g.user.id, 'forum_id': forum.id }
        is_forum_member = db.session.execute(is_forum_member_query, values).fetchone().is_member
    
    if (not is_forum_member and forum.password is not None):
        return render_template('forum/forum_password_prompt.html', forum=forum)
    if (not is_forum_member and forum.password is None):
        flash('You are not a member of this private forum')
        return redirect(url_for("forum.index"))
    getTopics = 'SELECT * FROM topic WHERE forum_id = (:forum_id)'
    topics = db.session.execute(getTopics, { "forum_id": forum_id }).fetchall()
    return render_template('forum/forum.html', forum=forum, topics=topics)

@forum_blueprint.route('/forum/create', methods=['GET'])
@login_required
def forumForm():
    return render_template('forum/create_forum.html')

@forum_blueprint.route('/forum', methods=['POST'])
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

