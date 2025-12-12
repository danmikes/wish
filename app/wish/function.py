import os
from flask import current_app, flash
from flask_login import current_user
from PIL import Image
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename
from .model import Wish
from ..util.logger import log
from .. import db

DIMENSION_MAX = 400

def get_upload_folder():
  return current_app.config['UPLOAD_FOLDER']

def allowed_file(file_name):
  return '.' in file_name and file_name.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def file_exists(file_name):
  file_path = os.path.join(get_upload_folder(), file_name)
  return os.path.exists(file_path)

def resize_image(image, dimension_max=DIMENSION_MAX):
  width, height = image.size

  if width > height:
    new_width = dimension_max
    new_height = int((height / width) * new_width)
  else:
    new_height = dimension_max
    new_width = int((width / height) * new_height)

  return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

def save_file(file):
  file_name = secure_filename(file.filename)
  file_path = os.path.join(get_upload_folder(), file_name)
  os.makedirs(get_upload_folder(), exist_ok=True)

  try:
    with Image.open(file) as image:
      if image.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', image.size, (255,255,255))
        if image.mode == 'P':
          image = image.convert('RGBA')
          background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
          image = background

      image_resized = resize_image(image)
      image_resized.save(file_path, dpi=(72, 72), quality=85, optimize=True)
      return file_name
  except Exception as e:
    flash(f'Error saving file: {e}', 'warning')
    return None

def delete_file(file_name):
  file_path = os.path.join(get_upload_folder(), file_name)

  try:
    os.remove(file_path)
    log.info(f'File removed: {file_name}')
    return None
  except Exception as e:
    log.info(f'File not removed: {file_name} : {e}')

  return file_name

def fill_wish(form, wish=None):
  wish = wish or Wish(
    owner=current_user,
    description='',
    url=None,
    price=None,
    image=None
  )
  wish.description = form.description.data
  wish.url = Wish.clean_url(form.url.data) if form.url.data else None
  wish.price = form.price.data

  # if form.image.data:
  #   wish.image = form.image.data

  return wish

def save_wish(wish=None):
  if wish is None:
    flash('No wish', 'warning')
    return False

  try:
    if wish.id is None:
      db.session.add(wish)
    db.session.commit()
    flash('Wish saved', 'info')
    return True
  except SQLAlchemyError as e:
    db.session.rollback()
    flash(f'Wish not saved: {str(e)}', 'info')
    return False

def delete_wish(wish):
  try:
    if wish.image:
      delete_file(wish.image)
    db.session.delete(wish)
    db.session.commit()
    return None
  except Exception as e:
    db.session.rollback()
    return wish

def process_wish(form, wish=None):
  if form.validate_on_submit():
    data = form.image.data
    new_image = data.filename if data else None
    old_image = wish.image if wish else None
    saved_image = None

    marked_for_deletion = form.marked_for_deletion.data == 'true'

    try:
      with db.session.begin_nested():
        if old_image:
          if marked_for_deletion:
            delete_file(old_image)
            if wish:
              wish.image = None

        if new_image:
          if not allowed_file(new_image):
            flash('Invalid file type', 'warning')
            return False

          if file_exists(new_image):
            flash('File exists', 'warning')
            return False

          saved_image = save_file(data)
          if not saved_image:
            raise Exception('File not saved')

        if wish is None:
          wish = fill_wish(form)
        else:
          wish = fill_wish(form, wish)

        if saved_image:
          wish.image = saved_image

        if wish.id is None:
          db.session.add(wish)

      db.session.commit()
      flash('Wish saved', 'info')
      return True

    except SQLAlchemyError as e:
      db.session.rollback()
      if saved_image:
        delete_file(saved_image)
      flash(f'Wish not saved: {str(e)}', 'warning')
      return False

    except Exception as e:
      db.session.rollback()
      if saved_image:
        delete_file(saved_image)
      flash(f'Error processing wish: {str(e)}', 'warning')
      return False

  return False

def add_wish(form):
  return process_wish(form)

def edit_wish(form, wish):
  return process_wish(form, wish)

def toggle_wish(wish):
  try:
    if wish.is_buyer:
      wish.buyer = None
      flash('Wish cancelled', 'warning')
    else:
      wish.buyer = current_user
      flash('Wish bought', 'info')
    db.session.commit()
    return True
  except SQLAlchemyError as e:
    db.session.rollback()
    flash('Wish not updated', 'warning')
    return False
