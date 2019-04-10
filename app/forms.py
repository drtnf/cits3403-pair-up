from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, regexp, EqualTo
from app.models import Lab

'''class to hold elements and validators for login form'''
class LoginForm(FlaskForm):
  student_number = StringField('Student Number', validators=[DataRequired(), regexp('^\d{8}$',message='must by 8 digits')])
  pin = PasswordField('Pin Code', validators=[regexp('^\d{4}$',message='must be 4 digits')])
  remember_me = BooleanField('Remember Me')
  submit =SubmitField('Sign In')

'''class to hold elements and validators for registration form'''
class RegistrationForm(FlaskForm):
  student_number = StringField('Student Number', validators=[DataRequired(), regexp('^\d{8}$', message='must be 8 digits')])
  prefered_name = StringField('Prefered Name', validators=[])
  pin =PasswordField('Current Pin',validators=[regexp('^\d{4}$',message='must be four digits')],default='0000')
  new_pin = PasswordField('New Pin', validators=[regexp('^\d{4}$', message='must be four digits')])
  new_pin2 = PasswordField('Confirm Pin', validators=[EqualTo('new_pin')])
  submit = SubmitField('Sign up')


'''Class to hold form elements for project registration and editting'''
class ProjectForm(FlaskForm):
  partner_number = StringField('Student Number', validators=[DataRequired(),regexp('^\d{8}$')],default='00000000')
  project_description = StringField('Project Description', validators=[DataRequired()])
  lab = SelectField('Demonstration Laboratory', choices = [])
  submit = SubmitField('Submit project')



