from enum import Enum, auto

class AllowedExtension(Enum):
  PNG = auto()
  JPG = auto()
  JPEG = auto()
  GIF = auto()

  @classmethod
  def as_set(cls):
    return {ext.name.lower() for ext in cls}
