import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import create_app, db
app = create_app()

with app.app_context():
  db.drop_all()
  print("Tables dropped")
  db.create_all()
  print("Tables created")
