import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
                SECRET_KEY='dev',
                SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://postgres:password123@localhost:4321/postgres',
                SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    app.config.from_pyfile('config.py', silent=True)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    db.init_app(app)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        result = db.session.execute("SELECT * FROM account")
        print(dir(result))
        account = result.fetchone()
        return f'{account.username}, {account.password}'

    return app
    