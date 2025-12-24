# fix_migrations_final.py
import os
import sys

os.environ['FLASK_APP'] = 'wsgi:application'

from wsgi import application

with application.app_context():
  from app import db
  from sqlalchemy import create_engine, text, inspect
  
  print("Starting migration fix...")
  
  # Get database URL
  db_url = application.config['SQLALCHEMY_DATABASE_URI']
  print(f"Database: {db_url}")
  
  # Ensure check_same_thread is set
  if 'sqlite' in db_url and 'check_same_thread=False' not in db_url:
    db_url = db_url + ('?check_same_thread=False' if '?' not in db_url else '&check_same_thread=False')
  
  # Create engine with proper settings
  engine = create_engine(db_url, connect_args={'check_same_thread': False})
  
  # Check current state
  inspector = inspect(engine)
  tables = inspector.get_table_names()
  print(f"\nTables found: {tables}")
  
  # Step 1: Create alembic_version table if missing
  if 'alembic_version' not in tables:
    print("\n1. Creating alembic_version table...")
    with engine.begin() as conn:
      conn.execute(text('''
        CREATE TABLE alembic_version (
          version_num VARCHAR(32) NOT NULL PRIMARY KEY
        )
      '''))
    print("   ✅ Created")
  else:
    print("\n1. ✅ alembic_version table exists")
  
  # Step 2: Check wish table
  print("\n2. Checking wish table...")
  if 'wish' in tables:
    columns = [col['name'] for col in inspector.get_columns('wish')]
    print(f"   Columns: {columns}")
    
    if 'price' not in columns:
      print("   Adding price column...")
      with engine.begin() as conn:
        conn.execute(text('ALTER TABLE wish ADD COLUMN price INTEGER;'))
      print("   ✅ Added price column")
    else:
      print("   ✅ Price column exists")
  else:
    print("   ❌ Wish table not found")
  
  # Step 3: Record migration
  print("\n3. Recording migration...")
  migration_id = 'c3f54bf7a5c6'
  
  with engine.connect() as conn:
    result = conn.execute(
      text(f"SELECT version_num FROM alembic_version WHERE version_num = '{migration_id}'")
    ).fetchone()
    
    if not result:
      with engine.begin() as conn:
        conn.execute(
          text(f"INSERT INTO alembic_version (version_num) VALUES ('{migration_id}')")
        )
      print(f"   ✅ Recorded migration {migration_id}")
    else:
      print(f"   ✅ Migration {migration_id} already recorded")
  
  # Final check
  print("\n4. Final verification...")
  with engine.connect() as conn:
    result = conn.execute(text('SELECT version_num FROM alembic_version')).fetchall()
    versions = [r[0] for r in result]
    print(f"   Applied migrations: {versions}")
  
  print("\n" + "=" * 60)
  print("✅ MIGRATION FIX COMPLETE")
  print("=" * 60)
