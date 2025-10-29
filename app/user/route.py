from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required, logout_user
from .form import LoginForm, RegistrationForm
from .model import User
from .function import handle_remove, handle_login, handle_register
from ..util.logger import log

user = Blueprint('user', __name__, url_prefix='/user', static_folder='.', template_folder='.')

@user.route('/all', methods=['GET'])
@login_required
def users():
  users_they = User.query.all()
  users_sorted = sorted(users_they, key=lambda user: user.username)
  return render_template('view.htm', users_they=users_sorted, page='view')

@user.route('/login', methods=['GET', 'POST'])
def user_login():
  if current_user.is_authenticated:
    return redirect(url_for('wish.wishes'))

  form = LoginForm()
  result = handle_login(form, request)
  if result:
    return result
  return render_template('login.htm', form=form, page='login')

@user.route('/logout', methods=['GET'])
@login_required
def user_logout():
  logout_user()
  flash('You logged-out', 'info')
  return redirect(url_for('user.user_login'))

@user.route('/all/json', methods=['GET'])
@login_required
def users_json():
  users = User.query.all()
  user_list = [user.to_dict() for user in users]
  return jsonify(user_list)
