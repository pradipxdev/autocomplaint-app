from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, Email
from flask_wtf.file import FileField, FileAllowed

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class ComplaintForm(FlaskForm):
    issue = StringField('Issue', validators=[DataRequired()])
    against = StringField('Against', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    file = FileField('Attach File', validators=[FileAllowed(['jpg', 'png', 'pdf', 'docx'])])
    submit = SubmitField('Submit')
