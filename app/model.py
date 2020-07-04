import os

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask import Flask

from flask_migrate import Migrate


def create_app():
    app = Flask(
        __name__,
        instance_relative_config=True,
        static_url_path=''
    )
    app.config.from_mapping(
        SECRET_KEY='!A7mVCJgdb*ojXhavC^9EiQQFXyLKtQ&c#ffEw#vrteW5qS*J$*7',
        SQLALCHEMY_DATABASE_URI='sqlite:///crypt.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    from flask_sslify import SSLify
    if 'DYNO' in os.environ:  # only trigger SSLify if the app is running on Heroku
        sslify = SSLify(app)

    # from app.model import migrate
    # migrate.init_app(app, db)

    return app


app = create_app()
db = SQLAlchemy(app)
db.init_app(app)
# migrate = Migrate()


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.String(512), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __init__(self, title, body):
        self.title = title
        self.body = body


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    notes = db.relationship('Note', backref='owner')

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __init__(self, username, password):
        self.username = username
        self.password = password


