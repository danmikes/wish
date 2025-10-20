import os
import shutil
from flask import Blueprint, current_app, jsonify, request, send_from_directory
from flask_login import login_required
from git import Repo
from ..util.logger import log
from ..wish.model import Wish
from .function import delete_image, format_date
from app import db

util = Blueprint('util', __name__, url_prefix='/util', static_folder='.', template_folder='.')

@util.route('/file/<path:filename>', methods=['GET'])
@login_required
def upload_file(filename):
  return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@util.route('/file/delete/<int:wish_id>', methods=['GET', 'DELETE'])
@login_required
def delete_file(wish_id):
  wish = Wish.query.get_or_404(wish_id)

  if wish.image:
    delete_image(wish.image)
    wish.image = None
    db.session.commit()

    return jsonify(success=True)

  return jsonify(success=False), 404

@util.route('/file/all/json', methods=['GET'])
@login_required
def files_json():
  folder_upload = current_app.config['UPLOAD_FOLDER']
  files_data = []
  for filename in os.listdir(folder_upload):
    if filename != '.DS_Store':
      file_path = os.path.join(folder_upload, filename)
      file_stats = os.stat(file_path)
      files_data.append({
        'name': filename,
        'size': file_stats.st_size,
        'modified': format_date(file_stats.st_mtime),
        'created': format_date(file_stats.st_ctime),
      })
  return jsonify(files=files_data)

@util.route('/update', methods=['POST'])
def update():
  if request.method == 'POST':
    repo = Repo(current_app.config['WORKING_DIRECTORY'])
    origin = repo.remotes.origin
    origin.fetch()
    repo.git.reset('--hard', 'origin/main')

    os.system(f"touch {current_app.config['WSGI_PATH']}")
    return 'PythonAnywhere updated', 200
  else:
    return 'Invalid request', 405
