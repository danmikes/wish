#!/usr/bin/env python3
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.insert(0, project_dir)

# Test file creation first
test_path = "/Users/dan/app/wish/instance/test_python.txt"
print(f"Testing file creation at: {test_path}")

try:
  with open(test_path, 'w') as f:
    f.write("test")
  print("✓ File creation successful")
  os.remove(test_path)
  print("✓ File deletion successful")
except Exception as e:
  print(f"✗ File creation failed: {e}")

from app import create_app, db
from app.user.model import User
from app.wish.model import Wish

app = create_app()
with app.app_context():
  db.drop_all()
  db.create_all()
  
  user = User(username='daniel', password='daniel')
  wish = Wish(owner=user, description='wish')
  
  db.session.add(user)
  db.session.add(wish)
  db.session.commit()
  
  print("Database initialized")
