from flask import Blueprint, redirect, render_template, session, url_for
from flask_login import current_user

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
