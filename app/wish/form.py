from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import BooleanField, DecimalField, FileField, HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, URL
from ..util.field_length import FieldLength, length_max

IMAGE_ONLY = 'Images only'

class WishForm(FlaskForm):
  id = HiddenField('ID')
  description = TextAreaField('Description', validators=[
      DataRequired(),
      Length(max=FieldLength.MEDIUM.value, message=length_max(FieldLength.MEDIUM))
    ])
  price = DecimalField('Price', validators=[
      Optional(),
      NumberRange(min=0)
    ],
    places=2)
  url = StringField('Link', validators=[
      Optional(),
      URL(message="Enter valid URL")
    ])
  image = FileField('Image', validators=[
      Optional(),
      FileAllowed(['gif', 'jpg', 'jpeg', 'png'
    ],
    message=IMAGE_ONLY)])
  submit = SubmitField('Save')
  marked_for_deletion = HiddenField('Marked for Deletion', default='false')
