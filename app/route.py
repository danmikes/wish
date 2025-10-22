import os
from flask import Blueprint, redirect, request, session, url_for
from flask_login import current_user
from git import Repo

base = Blueprint('base', __name__, static_folder='.', template_folder='.')

@base.route('/')
def index():
  if current_user.is_authenticated:
    return redirect(url_for('wish.wishes'))
  else:
    return redirect(url_for('user.user_login'))

# default = color
@base.route('/toggle_theme/<theme>')
def toggle_theme(theme):
  session['theme'] = theme
  return redirect(url_for('base.index'))

# default = medium
@base.route('/toggle_font/<font>')
def toggle_font(font):
  session['font'] = font
  return redirect(url_for('base.index'))

# default = english
@base.route('/toggle_lang/<lang>')
def toggle_lang(lang):
  session['lang'] = lang
  return redirect(url_for('base.index'))

@base.route('/health')
def health():
  return {'status': 'healthy'}, 200

@base.route('/update')
def update():
  auth_header = request.headers.get('Authorization')
  if not auth_header or not auth_header.startswith('Bearer '):
    return 'Missing or invalid Authorization header', 401

  token = auth_header.replace('Bearer ', '')
  token_expect = os.environ.get('DEPLOY_TOKEN')
  if token != token_expect:
    return 'Invalid token', 401

  work_dir = os.environ.get('WORK_DIR')
  repo = Repo(work_dir)
  origin = repo.remotes.origin
  origin.fetch()
  repo.git.reset('--hard', 'origin/main')

  wsgi_path = os.environ.get('WSGI_PATH')
  os.system(f'touch {wsgi_path}')
  return 'Updated successfully', 200
