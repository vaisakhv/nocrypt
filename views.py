from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, TextAreaField, SubmitField


class LoginForm(FlaskForm):
    username = StringField('username',
                           [validators.DataRequired("Please enter your username"), validators.Length(min=4)],
                           render_kw={'placeholder': 'Username'})
    password = PasswordField('password',
                             [validators.DataRequired("Please enter you password"), validators.Length(min=7)],
                             render_kw={'placeholder': 'password'})


class SignupForm(FlaskForm):
    username = StringField('username',
                           [validators.DataRequired("Please enter your username"), validators.Length(min=4)],
                           render_kw={'placeholder': 'Username'})
    password = PasswordField('password',
                             [validators.DataRequired("Please enter you password"), validators.Length(min=7)],
                             render_kw={'placeholder': 'password'})
    confirm_password = PasswordField('confirm_password',
                                     [validators.DataRequired("Please re-enter you password"), validators.Length(min=7)],
                                     render_kw={'placeholder': 're-enter password'})

