from flask import Blueprint, url_for

forum_blueprint = Blueprint('forum', __name__)

from . import forum, topic, comment
