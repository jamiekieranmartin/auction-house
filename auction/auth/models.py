from .. import db
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    contactnumber = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(250), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def __init__(self, form):
        '''Initialiser using form'''
        self.email = form.email.data
        self.name = form.user_name.data
        self.contactnumber = form.contactnumber.data
        self.address = form.address.data
        self.password_hash = generate_password_hash(form.password.data)


class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.id = -1
