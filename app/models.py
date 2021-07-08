from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(length=80), nullable=False)
    last_name = db.Column(db.String(length=80), nullable=False)
    email = db.Column(db.String(length=255), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=255), nullable=False)
    notes = db.relationship('Note', back_populates="user")

    def __init__(self, name: str, email: str, password: str):
        [self.first_name, self.last_name] = name.rsplit(" ", 1)
        self.email = email
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='notes')
    text = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now,
                           onupdate=datetime.now)
