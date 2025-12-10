from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import current_app, redirect, request, url_for
from markupsafe import Markup
from wtforms import PasswordField, StringField

class CustomAdminView(AdminIndexView):
  @expose('/')
  def index(self):
    return self.render('admin/index.html')

  def is_accessible(self):
    return current_user.is_authenticated and current_user.id == current_app.config['ADMIN_ID']

  def inaccessible_callback(self, name, **kwargs):
    return redirect(url_for('user.login', next=request.url))

admin = Admin(
    name='Home',
    url='/admin',
    index_view=CustomAdminView(name='Home', url='/admin', endpoint='admin')
)

class SecureModelView(ModelView):
  def is_accessible(self):
    return current_user.is_authenticated and current_user.id == current_app.config['ADMIN_ID']

  def inaccessible_callback(self, name, **kwargs):
    return redirect(url_for('user.login', next=request.url))

class UserAdminView(SecureModelView):
  column_list = ['id', 'username']

  def _is_owner_formatter(self, context, model, name):
    from app.wish.model import Wish
    wish_count = Wish.query.filter_by(owner_id=model.id).count()
    return f'Yes ({wish_count})' if wish_count > 0 else 'No'

  def _is_buyer_formatter(self, context, model, name):
    from app.wish.model import Wish
    buyer_count = Wish.query.filter_by(buyer_id=model.id).count()
    return f'Yes ({buyer_count})' if buyer_count > 0 else 'No'

  column_formatters = {
    'is_owner': _is_owner_formatter,
    'is_buyer': _is_buyer_formatter,
  }

  column_list = ['id', 'username', 'is_owner', 'is_buyer']

  column_searchable_list = ['username']
  column_filters = ['username']
  column_default_sort = ('id')

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
      form.current_password.data = '••••••••' # type: ignore

  def on_model_change(self, form, model, is_created):
    if form.password.data: # type: ignore
      model.set_password(form.password.data) # type: ignore

class WishAdminView(SecureModelView):
  column_list = ['id', 'description', 'domain', 'owner.username', 'buyer.username', 'image_preview']
  column_labels = {
    'owner.username': 'Owner',
    'buyer.username': 'Buyer',
    'image_preview': 'Image'
  }

  column_searchable_list = ['description', 'url']
  column_filters = ['owner.username', 'buyer.username']
  column_default_sort = ('id')

  def image_preview_formatter(self, context, model, name):
    if model.image:
      try:
        image_url = url_for('util.upload_file', filename=model.image)
      except:
        image_url = f'/util/file/{model.image}'

      html = f'<img src="{image_url}" width="50" height="50" style="object-fit: cover; border-radius: 4px;">'
      return Markup(html)
    return "-"

  def domain_formatter(self, context, model, name):
    if hasattr(model, 'domain') and model.domain:
      return model.domain
    if model.url:
      from tldextract import extract
      extracted = extract(model.url)
      return f"{extracted.domain}.{extracted.suffix}"
    return "-"

  column_formatters = {
    'image_preview': image_preview_formatter,
    'domain': domain_formatter,
  }

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

  def delete_model(self, model):
    if model.image:
      from app.util.function import delete_image
      delete_image(model.image)
    return super().delete_model(model)

def init_admin(app, db_param):
  from app.user.model import User
  from app.wish.model import Wish

  global db
  db = db_param

  admin.init_app(app)

  @app.after_request
  def inject_admin_redirect(response):
    if (request.path.startswith('/admin') and
      response.content_type == 'text/html; charset=utf-8'):

      css_code = """
      <style>
      /* Hide the admin Home nav item immediately */
      .navbar-nav a[href="/admin/"] {
          display: none !important;
      }
      </style>
      """

      js_code = """
      <script>
      document.addEventListener('DOMContentLoaded', function() {
          var brand = document.querySelector('.navbar-brand');
          if (brand && brand.href.endsWith('/admin')) {
              brand.href = '/';
          }
      });
      </script>
      """

      if response.data:
        response.data = response.data.replace(b'</head>', css_code.encode() + b'</head>')
        response.data = response.data.replace(b'</body>', js_code.encode() + b'</body>')
    return response

  admin.add_view(UserAdminView(User, db.session, endpoint='users'))
  admin.add_view(WishAdminView(Wish, db.session, endpoint='wishes'))
