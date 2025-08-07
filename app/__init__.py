<<<<<<< HEAD
import os
from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
=======
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

    db.init_app(app)


    from .routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()


    return app
>>>>>>> c1dfbe2 (Initial Flask project setup)
