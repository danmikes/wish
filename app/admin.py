from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import current_app, redirect, request, url_for
from wtforms import PasswordField, StringField

admin = Admin(name='Wish List Admin', url='/admin')

class SecureModelView(ModelView):
  def is_accessible(self):
    return current_user.is_authenticated and current_user.id == current_app.config['ADMIN_ID']

  def inaccessible_callback(self, name, **kwargs):
    return redirect(url_for('user.login', next=request.url))

class UserAdminView(SecureModelView):
  column_list = ['id', 'username']

  def _has_wishes_formatter(self, context, model, name):
    from app.wish.model import Wish
    wish_count = Wish.query.filter_by(owner_id=model.id).count()
    return f'Yes ({wish_count})' if wish_count > 0 else 'No'

  def _is_buyer_formatter(self, context, model, name):
    from app.wish.model import Wish
    buyer_count = Wish.query.filter_by(buyer_id=model.id).count()
    return f'Yes ({buyer_count})' if buyer_count > 0 else 'No'

  column_formatters = {
    'has_wishes': _has_wishes_formatter,
    'is_buyer': _is_buyer_formatter,
  }

  column_list = ['id', 'username', 'has_wishes', 'is_buyer']

  # form_columns = ['id', 'username', 'password', 'current_password']
  form_excluded_columns = ['password_hash', 'timestamp']

  form_extra_fields = {
    'password': PasswordField('New Password'),
    'current_password': StringField('Current Password Hash', render_kw={'readonly': True})
  }

  def on_form_prefill(self, form, id):
    from app.user.model import User
    user = db.session.get(User, id)
    if user:
      form.current_password.data = '••••••••'  # type: ignore

  def on_model_change(self, form, model, is_created):
    if form.password.data: # type: ignore
      model.set_password(form.password.data) # type: ignore

class WishAdminView(SecureModelView):
  def get_query(self):
    if current_user.id != 1:
      return self.session.query(self.model).filter(self.model.owner_id == current_user.id)
    return super().get_query()

  def get_count_query(self):
    if current_user.id != 1:
      return self.session.query(self.model).filter(self.model.owner_id == current_user.id)
    return super().get_count_query()

  def on_model_change(self, form, model, is_created):
    if is_created and current_user.id != 1:
      model.owner_id = current_user.id # type: ignore

def init_admin(app, db_param):
  from app.user.model import User
  from app.wish.model import Wish

  global db
  db = db_param

  admin.init_app(app)
  admin.add_view(UserAdminView(User, db.session, endpoint='users'))
  admin.add_view(WishAdminView(Wish, db.session, endpoint='wishes'))
