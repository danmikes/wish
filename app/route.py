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
  secret = os.environ.get('DEPLOY_SECRET')
  if request.args.get('secret') != secret:
    return 'Invalid secret', 401

  repo = Repo('/home/dmikes/wish')
  origin = repo.remotes.origin
  origin.fetch()
  repo.git.reset('--hard', 'origin/main')

  os.system("touch /var/www/dmikes_pythonanywhere_com_wsgi.py")
  return 'Updated successfully', 200
