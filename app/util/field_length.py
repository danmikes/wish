from enum import Enum

class FieldLength(Enum):
  MINI = 3
  SMALL = 20
  MEDIUM = 128
  LARGE = 255

def length_max(field_length=FieldLength.MEDIUM):
  max_chars = field_length.value if isinstance(field_length, FieldLength) else field_length
  return f'Maximum {max_chars} characters'
