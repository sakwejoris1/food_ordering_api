import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///site.db',  # database file in project root
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    db.init_app(app)

    # import blueprints
    from .routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()  # create database tables

    return app
