from flask import Flask, request, jsonify, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import UserForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'ohsosecret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False
debug=DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home():
    return redirect('/register')

@app.route('/register')
def register():
    form=UserForm()
    return render_template('register.html', form=form)
