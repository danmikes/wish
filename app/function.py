import json
import os
from flask import current_app, redirect, url_for
from flask_assets import Environment
from webassets.bundle import Bundle
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from .util.logger import log
from .util.enum import AllowedExtension

project_root = os.path.dirname(os.path.dirname(__file__))
db_path = os.path.join(project_root, 'instance', 'data.db')
os.makedirs(os.path.dirname(db_path), exist_ok=True)

csrf = CSRFProtect()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'user.user_login' # type: ignore

def config_app(app):
  app.config.update({
    'ADMIN_ID': 1,
    'ALLOWED_EXTENSIONS': AllowedExtension.as_set(),
    'SECRET_KEY': os.environ.get('SECRET_KEY', 'dev-fallback-key'),
    'SESSION_COOKIE_HTTPONLY': True,
    'SESSION_COOKIE_SAMESITE': 'Lax',
    'SESSION_COOKIE_SECURE': os.environ.get('FLASK_ENV') == 'production',
    'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}?check_same_thread=False',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'UPLOAD_FOLDER': os.path.join(app.root_path, 'upload'),
  })

  os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def initialise_extensions(app):
  csrf.init_app(app)
  db.init_app(app)
  login_manager.init_app(app)

def initialise_database(app):
  with app.app_context():
    db.create_all()

def register_blueprints(app):
  from .blueprint import register_route
  register_route(app)

def build_assets(app):
  assets = Environment(app)
  scss = Bundle('style.css',
                'color.scss',
                filters='libsass',
                output='all.css',
                depends='*.scss')
  assets.register("asset_css", scss)
  scss.build()

def build_admin(app, db):
  from .admin import init_admin
  init_admin(app, db)

def load_content(lang):
  file_path = os.path.join(current_app.root_path, 'content', f'{lang}.json')
  try:
    with open(file_path, 'r', encoding='utf-8') as f:
      return json.load(f)
  except FileNotFoundError:
    log.error(f'Content file not found: {file_path}')
    return {}

@login_manager.user_loader
def load_user(user_id):
  from .user.model import User
  return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
  return redirect(url_for('user.user_login'))
