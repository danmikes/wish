import os
import sys

os.environ['DEPLOY_TOKEN'] = 'fac648fa6a6329e71b6e076f9080b623'
os.environ['WSGI_PATH'] = '/var/www/dmikes_eu_pythonanywhere_com_wsgi.py'
os.environ['WORK_DIR'] = '/home/dmikes/wish'

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
  sys.path.insert(0, current_dir)

from app import create_app
application = create_app()
