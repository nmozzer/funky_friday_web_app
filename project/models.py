from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    type = db.Column(db.String(100))
    improvements = db.relationship('Improvement', back_populates='user')

class System(db.Model):
    __tablename__ = 'systems'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    state = db.Column(db.String(100))
    priority = db.Column(db.Integer)
    techStack = db.Column(db.String(100))
    description = db.Column(db.String(100))
    improvements = db.relationship('Improvement', back_populates='system', cascade="all, delete-orphan")


class Improvement(db.Model):
    __table_name__ = 'ideas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    system_id = db.Column(db.Integer, db.ForeignKey('systems.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    beans = db.Column(db.Integer)
    system = db.relationship('System', back_populates='improvements')
    user = db.relationship('User', back_populates='improvements')



