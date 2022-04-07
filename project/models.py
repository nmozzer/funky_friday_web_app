from flask_login import UserMixin
from . import db
from sqlalchemy.sql import func

class User(UserMixin, db.Model):    
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(1000), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    improvements = db.relationship('Improvement', back_populates='user')

    def __repr__(self):
        return f'<User {self.email}>'

class System(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    system_health = db.Column(db.String(100))
    priority = db.Column(db.Integer)
    language = db.Column(db.Text)
    tech_stack = db.Column(db.Text)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    improvements = db.relationship('Improvement', back_populates='system', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<System {self.name}>'


class Improvement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    system_id = db.Column(db.Integer, db.ForeignKey('systems.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    beans = db.Column(db.Integer)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    system = db.relationship('System', back_populates='improvements')
    user = db.relationship('User', back_populates='improvements')

    def __repr__(self):
        return f'<Improvement {self.name}>'


