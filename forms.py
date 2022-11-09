from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import InputRequired, Length

class UserForm(FlaskForm):
    username=StringField("Username", validators=[InputRequired(message="Input username"), Length(max=20, message="Username must be less than 20 characters")])
    password=PasswordField("Password", validators=[InputRequired(message="Input password")])
    email=EmailField("Email", validators=[InputRequired(message="Input email"), Length(max=50, message="Email too long")])
    first_name=StringField("First name", validators=[InputRequired(message="Input first name")])
    last_name=StringField("Last name", validators=[InputRequired(message="Input last name")])
    

class LoginForm(FlaskForm):
    username=StringField("Username", validators=[InputRequired(message="Input username"), Length(max=20, message="Username must be less than 20 characters")])
    password=PasswordField("Password", validators=[InputRequired(message="Input password")])
    
    

class FeedbackForm(FlaskForm):
    title=StringField("Title", validators=[InputRequired(message="Input title")])
    content=TextAreaField("Content", validators=[InputRequired(message="Input content")])