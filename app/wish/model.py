import tldextract
from flask_login import current_user
from urllib.parse import urlparse, urlunparse
from .. import db

class Wish(db.Model):
  __tablename__ = 'wish'

  id = db.Column(db.Integer, primary_key=True)

  description = db.Column(db.String(255), nullable=False)
  url = db.Column(db.String(255))
  image = db.Column(db.String(255))

  owner_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), index=True)
  owner = db.relationship('User', back_populates='wishes', foreign_keys=lambda: [Wish.owner_id])

  buyer_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'), index=True)
  buyer = db.relationship('User', back_populates='wishes_bought', foreign_keys=lambda: [Wish.buyer_id])

  def __init__(self, description, url=None, image=None, owner=None):
    self.description = description
    self.url = self.clean_url(url) if url else None
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
      extracted = tldextract.extract(self.url)
      return extracted.domain.lower()
    return None

  @staticmethod
  def clean_url(url):
    parsed = urlparse(url)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))

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
