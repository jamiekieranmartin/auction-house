from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, IntegerField
from wtforms.validators import InputRequired, Length, Email, EqualTo


# login form
class LoginForm(FlaskForm):
    user_name = StringField("User Name",
                            validators=[InputRequired('Enter user name')])
    password = PasswordField("Password",
                             validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")


# registration form
class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email = StringField(
        "Email Address",
        validators=[InputRequired(),
                    Email("Please enter a valid email")])
    contactnumber = IntegerField("Phone", validators=[InputRequired()])
    address = StringField("Address", validators=[InputRequired()])
    password = PasswordField("Password",
                             validators=[
                                 InputRequired(),
                                 EqualTo('confirm',
                                         message="Passwords should match")
                             ])
    confirm = PasswordField("Confirm Password", validators=[InputRequired()])
    submit = SubmitField("Register")
