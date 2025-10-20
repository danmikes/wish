import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import create_app, db
from app.user.model import User
from app.wish.model import Wish

app = create_app()
with app.app_context():
  db.session.query(Wish).delete()
  db.session.query(User).delete()
  db.session.commit()
  print("Database cleared")
