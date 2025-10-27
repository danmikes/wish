from flask_login import current_user
from sqlalchemy import event
from urllib.parse import urlparse
from .. import db

class Wish(db.Model):
  __tablename__ = 'wish'

  id = db.Column(db.Integer, primary_key=True)

  description = db.Column(db.String(255), nullable=False)
  url = db.Column(db.String(255))
  image = db.Column(db.String(255))

  owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True, nullable=False)
  owner = db.relationship('User', back_populates='wishes', foreign_keys=[owner_id])

  buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
  buyer = db.relationship('User', back_populates='wishes_bought', foreign_keys=[buyer_id])

  def __init__(self, description, url=None, image=None, owner=None):
    self.description = description
    self.url = url
    self.image = image
    if owner is not None:
      self.owner = owner

  @property
  def is_bought(self):
    return self.buyer is not None

  @property
  def is_buyer(self):
    return self.buyer == current_user

  @property
  def domain(self):
    if self.url:
      hostname = urlparse(self.url).hostname.replace('www.', '')
      return hostname.rsplit('.', 1)[0] if '.' in hostname else hostname
    return None

  def __repr__(self):
    return f'<Wish {self.id}: {self.description[:20]}... - {self.image} - {self.is_bought}>'

  def to_dict(self):
    return {
      'description': self.description,
      'url': self.url,
      'domain': self.domain,
      'image': self.image,
      'buyer': self.buyer.username if self.buyer else None,
      'owner': self.owner.username,
      'is_bought': self.is_bought,
      'is_buyer': self.is_buyer,
    }
