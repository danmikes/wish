from flask import Blueprint, redirect, render_template, request, session, url_for
from .util.logger import log

base = Blueprint('base', __name__, url_prefix='/', static_folder='.', template_folder='.')

@base.route('/')
def index():
  return render_template('index.htm')

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
