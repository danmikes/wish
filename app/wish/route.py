from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from ..util.flash import flash_errors
from ..user.model import User
from .form import WishForm
from .model import Wish
from .function import add_wish, delete_wish, edit_wish, toggle_wish

wish = Blueprint('wish', __name__, url_prefix='/wish', static_folder='.', template_folder='.')

@wish.route('/all', methods=['GET'])
@login_required
def wishes():
  users_all = User.query.all()
  users_they = [user for user in users_all if user.id != current_user.id]
  users_they.sort(key=lambda user: user.username.lower())

  return render_template('wish/view.htm', users_they=users_they)

@wish.route('/add', methods=['GET', 'POST'])
@login_required
def wish_add():
  form = WishForm()

  if request.method == 'POST':
    if add_wish(form):
      return redirect(url_for('wish.wishes'))

  flash_errors(form)
  return render_template('wish/form.htm', form=form, is_edit=False)

@wish.route('/edit/<int:wish_id>', methods=['GET', 'POST'])
@login_required
def wish_edit(wish_id):
  wish = Wish.query.get_or_404(wish_id)
  form = WishForm(obj=wish)

  if request.method == 'POST':
    if edit_wish(form, wish):
      return redirect(url_for('wish.wishes'))

  flash_errors(form)
  return render_template('wish/form.htm', form=form, wish=wish, is_edit=True)

@wish.route('/delete/<int:wish_id>', methods =['GET', 'DELETE'])
@login_required
def wish_delete(wish_id):
  wish = Wish.query.get_or_404(wish_id)

  try:
    delete_wish(wish)
    flash('Wish deleted', 'success')
  except Exception as e:
    flash('Wish not deleted', 'error')
  return redirect(url_for('wish.wishes'))

@wish.route('/toggle/<int:wish_id>', methods=['GET'])
@login_required
def wish_toggle(wish_id):
  wish = Wish.query.get_or_404(wish_id)
  toggle_wish(wish)

  return redirect(url_for('wish.wishes'))

@wish.route('/all/json', methods=['GET'])
@login_required
def wishes_json():
  wishes = Wish.query.all()
  wish_list = [wish.to_dict() for wish in wishes]
  return jsonify(wish_list)
