from enum import Enum

class FieldLength(Enum):
  MINI = 3
  SMALL = 20
  MEDIUM = 128
  LARGE = 255

def length_max(max=FieldLength.MEDIUM):
  return f'Maximum {max} characters'
