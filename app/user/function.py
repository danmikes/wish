from flask import flash, redirect, url_for
from flask_login import login_user
from urllib.parse import urlparse
from ..util.flash import flash_errors
from .. import db
from ..wish.model import Wish
from .model import User

def handle_login(form, request):
  if form.validate_on_submit():
    try:
      user = User.query.filter_by(username=form.username.data).first()
      if user and user.check_password(form.password.data):
        login_user(user)
        flash('You logged-in', 'info')
        next = request.args.get('next')
        if not next or urlparse(next).netloc != '':
          next = url_for('wish.wishes')
        return redirect(next)
      else:
        flash('Invalid credentials', 'warning')
    except Exception as e:
      flash('Login error; retry', 'warning')

  flash_errors(form)
  return None

def handle_register(form):
  if form.validate_on_submit():
    if User.query.filter_by(username=form.username.data).first():
      flash('Username exists; choose another.', 'warning')
    else:
      new_user = User(username=form.username.data, password=form.password.data)
      try:
        db.session.add(new_user)
        db.session.commit()
        flash('You registered', 'info')
        return redirect(url_for('user.users'))
      except Exception as e:
        db.session.rollback()
        flash('Registration failed', 'warning')

  flash_errors(form)
  return None

def handle_remove(user):
  wishes_bought = Wish.query.filter_by(buyer_id=user.id).all()
  for wish in wishes_bought:
    wish.buyer_id = None

  db.session.delete(user)

  try:
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    raise e
