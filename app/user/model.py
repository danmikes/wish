from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db
from app.wish.model import Wish

class User(UserMixin, db.Model):
  __tablename__ = 'user'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  password_hash = db.Column(db.String(128), nullable=False)
  timestamp = db.Column(db.DateTime, default=datetime.utcnow)

  wishes = db.relationship('Wish', back_populates='owner', cascade="all, delete-orphan", foreign_keys=lambda: [Wish.owner_id])
  wishes_bought = db.relationship('Wish', back_populates='buyer', foreign_keys=lambda: [Wish.buyer_id])

  def __init__(self, username, password):
    self.username = username
    self.set_password(password)

  def __repr__(self):
    return f'<User {self.id}: {self.username}>'

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

  def to_dict(self):
    return {
      'username': self.username,
      'wishes': [wish.description for wish in self.wishes.all()],
      'wishes_bought': [wish.description for wish in self.wishes_bought.all()],
    }

