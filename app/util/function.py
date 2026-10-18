import os
from datetime import datetime
from flask import current_app
from ..util.logger import log

def delete_image(file_name):
  folder_upload = current_app.config['UPLOAD_FOLDER']
  file_path = os.path.join(folder_upload, file_name)

  try:
    os.remove(file_path)
    log.info(f'File removed: {file_name}')
  except Exception as e:
    log.info(f'File not removed: {file_name}: {e}')

  return True

def format_date(time):
  return datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
