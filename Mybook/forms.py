from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Mybook.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=5, max=20)])
    email = EmailField('Email',
                        validators=[DataRequired(), Email('Enter a valid email address')])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')



class LoginForm(FlaskForm):
    username = StringField('Username',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Login')

class PostForm(FlaskForm):
    picture = FileField('Update Profile Picture', validators=[DataRequired(),FileAllowed(['jpg', 'png'])])
    title = StringField('Title',validators=[DataRequired(), Length(max=15)])
    content = TextAreaField('Content',validators=[DataRequired()])
    submit = SubmitField('Post')