import os
from flask import Flask
from .db import db
from . import auth
from . import search
from .forum import forum_blueprint
from dotenv import load_dotenv

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    FLASK_ENV = os.getenv('FLASK_ENV')
    if FLASK_ENV == 'development':
        app.config.from_mapping(
          SECRET_KEY='dev',
          SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://postgres:password123@localhost:5432/postgres',
          SQLALCHEMY_TRACK_MODIFICATIONS=False
        )
    else:
        DATABASE_URL = os.getenv("DATABASE_URL")  # or other relevant config var
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        app.config.from_mapping(
          SECRET_KEY=os.environ.get('SECRET_KEY'),
          SQLALCHEMY_DATABASE_URI=DATABASE_URL,
          SQLALCHEMY_TRACK_MODIFICATIONS=False
        )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(search.bp)
    app.register_blueprint(forum_blueprint)
    app.add_url_rule('/', endpoint='index')

    return app
    
