from . import forum_blueprint
from flask import (
    flash, g, redirect, render_template, request, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError
from flaskr.auth import login_required, admin_required
from flaskr.db import db

@forum_blueprint.route('/forum/<forum_id>/member', methods=["POST"])
@login_required
def register_private_forum(forum_id):
    if g.user.is_admin:
        try:
            username = request.form['username']
            getUser = 'SELECT * FROM account WHERE username = :username'
            user = db.session.execute(getUser, { 'username': username }).fetchone()
            account_id = user.id
        except:
            error = f'User {username} does not exist'
            flash(error)
            return redirect(url_for('index'))
    else:
        password = request.form['password']
        getForum = 'SELECT * FROM forum WHERE id = :forum_id'
        forum = db.session.execute(getForum, { 'forum_id': forum_id }).fetchone()
        if not check_password_hash(forum['password'], password):
            error = 'Incorrect password'
            flash(error)
            return redirect(url_for('index'))
        account_id = g.user.id
    try:
        insertUserToForum = 'INSERT INTO private_forum_account (account_id, forum_id) VALUES (:account_id, :forum_id)'
        values = { 'account_id': account_id, 'forum_id': forum_id }
        db.session.execute(insertUserToForum, values)
        db.session.commit()
        return redirect(url_for('forum.forum', forum_id=forum_id))
    except IntegrityError:
        error = 'Something went wrong'
        flash(error)
        return redirect(url_for('index'))


@forum_blueprint.route('/forum/<forum_id>/member', methods=["GET"])
@login_required
@admin_required
def private_forum_form(forum_id):
    getForum = 'SELECT * FROM forum WHERE id = :forum_id'
    forum = db.session.execute(getForum, { 'forum_id': forum_id }).fetchone()
    return render_template('forum/add_private_forum_member.html', forum=forum)


    
