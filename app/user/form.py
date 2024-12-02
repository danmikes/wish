from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length
from ..util.field_length import FieldLength, length_max

common_validators = [
  DataRequired(),
  Length(min=FieldLength.MINI.value, max=FieldLength.SMALL.value, message=length_max(FieldLength.SMALL))
]

class LoginForm(FlaskForm):
  username = StringField('Username', validators=common_validators)
  password = PasswordField('Password', validators=common_validators)
  submit = SubmitField('Log-In')

class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=common_validators)
  password = PasswordField('Password', validators=common_validators)
  confirm_password = PasswordField('Confirm Password', validators=[
    *common_validators,
    EqualTo('password'),
  ])
  submit = SubmitField('Register')
