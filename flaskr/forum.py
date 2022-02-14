from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required

bp = Blueprint('forum', __name__)

@bp.route('/')
def index():
    return render_template('forum/index.html')
