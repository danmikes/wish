from flask import Flask, current_app, g, session
from .function import (
  build_admin,
  build_assets,
  config_app,
  initialise_extensions,
  initialise_database,
  load_content,
  register_blueprints,
)
from .function import db

def create_app():
  app = Flask(__name__, static_folder='/', template_folder='/')

  @app.before_request
  def before_request():
    lang = session.get('lang', 'en')
    g.content = load_content(lang)

  @app.context_processor
  def inject_content():
    return dict(content=g.content)

  config_app(app)
  initialise_extensions(app)
  initialise_database(app)
  register_blueprints(app)
  build_admin(app, db)
  build_assets(app)

  return app
