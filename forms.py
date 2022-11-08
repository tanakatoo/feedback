from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length

class UserForm(FlaskForm):
    username=StringField("Username", validators=[InputRequired(), Length(max=20)])
    password=PasswordField("Password", validators=[InputRequired()])
    email=StringField("Email", validators=[InputRequired(), Length(max=50)])
    first_name=StringField("First name", validators=[InputRequired()])
    last_name=StringField("Last name", validators=[InputRequired()])