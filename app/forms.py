from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, regexp

class LoginForm(FlaskForm):
    studentNumber = StringField('Student Number', validators=[DataRequired(), regexp('^\d{8}$')])
    pinCode = PasswordField('Pin Code', validators=[regexp('^\d{4}$')])
    remember_me = BooleanField('Remember Me')
    submit =SubmitField('Sign In')

class projectForm(FlaskForm):
    cits3403Days = [(1,'Monday May 20, 2-4, CSSE:2.01'),(2,'Wednesday May 22, 2-4, ELEC:1.51'),(3,'Wednesday May 24, 2-4, CSSE:2.01')]
    cits5505Days = [(4,'Wednesday May 22, 12-2, CSSE:2.03')]
    cits3403Times = [(1,'4.00-4.05')]
    partnerNumber = StringField('Student Number', validators=[DataRequired()])
    projectDescription = StringField('Project Description', validators=[DataRequired()])
    demonstrationTute = SelectField('Laboratory', choices=cits3403Days)
    demonstrationTime = SelectField('Time', choices=cits3403Times)
    #put in dynamic update here

