import logging
import os

APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

RESET = '\033[0m'
COLORS = {
  'DEBUG': '\033[34m',    # Blue
  'INFO': '\033[32m',     # Green
  'WARNING': '\033[33m',  # Yellow
  'ERROR': '\033[31m',    # Red
  'CRITICAL': '\033[41m', # Red background
}

class Formatter(logging.Formatter):
  def format(self, record):
    log_color = COLORS.get(record.levelname, RESET)

    full_path = record.pathname
    try:
      short_path = os.path.relpath(full_path, APP_ROOT)
    except ValueError:
      short_path = full_path

    original_pathname = record.pathname
    record.pathname = short_path
    message = super().format(record)
    record.pathname = original_pathname

    return f'{log_color}{message}{RESET}'

log = logging.getLogger('app')
log.setLevel(logging.DEBUG)

formatter = Formatter('[%(levelname)s] : %(name)s/%(pathname)s:%(lineno)d - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
log.addHandler(console_handler)

# file_handler = logging.FileHandler('app.log')
# file_handler.setLevel(logging.INFO)
# file_handler.setFormatter(formatter)
# log.addHandler(file_handler)
