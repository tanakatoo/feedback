from flask import Flask, request, jsonify, redirect, render_template, flash, session, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import UserForm, LoginForm, FeedbackForm
from helpers import Helpers
from flask_mail import Mail, Message
from secrets import token_urlsafe

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'ohsosecret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False
debug=DebugToolbarExtension(app)

MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'karmen.tanaka@gmail.com'
MAIL_PASSWORD = 'stupidKT777!'
mail = Mail(app)
connect_db(app)

@app.route('/password-reset', methods=['GET','POST'])
def email():
    if request.method=='GET':
        s=token_urlsafe()
        print('*********')
        print(s)
        return render_template('password_reset.html')
    else:
        email=request.form['email']
        email_valid=User.query.filter_by(email=email).first()
        if email_valid:
            # send email to reset password
            s=token_urlsafe()
            print('*********')
            print(s)
            msg=Message("hello", sender="karmen.tanaka@gmail.com",recipients=["karmen.tanaka@gmail.com"])
          
            msg.body = "hello from text"
            msg.html = "<h1>hello from html</h1>"
            mail.send(msg)
            mail.send(msg)
            flash('password email is sent')
            return redirect('/login')
        else:
            flash('you are not registered yet')
            return redirect('/password-reset')

@app.route('/')
def home():
    return redirect('/register')

@app.route('/register', methods=["GET","POST"])
def register():
    form=UserForm()
    if form.validate_on_submit():
        user={"username":form.username.data,
            "password":form.password.data,
            "email":form.email.data,
            "first_name":form.first_name.data,
            "last_name":form.last_name.data
              }
        new_user =User.register(user)
        if new_user:
            Helpers.write_to_session("username",new_user.username)
            flash(f'Welcome {new_user.first_name}, account is created!')
            return redirect(f'/users/{new_user.username}')
        else:
            flash('username or email is taken')
            return render_template('register.html',form=form)
    else:
        return render_template('register.html',form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
    
        u=User.login(username,password)
        Helpers.write_to_session("username",u.username)
        flash(f'Welcome back {u.first_name}!')
        return redirect(f'/users/{username}')
    else:
        return render_template('login.html',form=form)

@app.route('/users/<username>')
def secret(username):
    if session.get('username'):
        u=User.get_user(username)
        
        return render_template('secret.html',u=u,feedback=u.feedback)
    else:
        return redirect('/login')

@app.route('/users/<username>/delete')
def delete_user(username):
    if session.get('username'):
        User.delete_user(username)

    return redirect('/login')

@app.route('/logout')
def logout():
    if session.get('username'):
        session.pop('username')
    return redirect ('/')


@app.route('/users/<username>/feedback/add', methods=['GET','POST'])
def add_feedback(username):
    if session.get('username'):
    
        form=FeedbackForm()
        if form.validate_on_submit():
            title=form.title.data
            content=form.content.data
        
            res=Feedback.add_feedback(title=title,content=content,username=username)

            flash('Feedback recorded')
            return redirect(f'/users/{username}')
        else:
            return render_template('feedback_add.html',form=form, username=username)
    else:
        return redirect('/login')
        

@app.route('/feedback/<feedback_id>/update', methods=['GET','POST'])
def update_feedback(feedback_id):
    username=session.get('username')
    f=Feedback.get_feedback(feedback_id)
    if session.get('username') and f.author.username==session.get('username'):
        form=FeedbackForm(obj=f)
        if form.validate_on_submit():
            title=form.title.data
            content=form.content.data
            username=session.get('username')
            res=Feedback.update_feedback(feedback_id=feedback_id, title=title,content=content)

            flash('Feedback updated')
            return redirect(f'/users/{username}')
        else:
            return render_template('feedback_edit.html',form=form, feedback=f)
    else:
        return redirect(f'/users/{username}')
    
    
@app.route('/feedback/<feedback_id>/delete', methods=['GET','POST'])
def delete_feedback(feedback_id):
    username=session.get('username')
    f=Feedback.get_feedback(feedback_id)
    if session.get('username') and f.author.username==session.get('username'):
        f=Feedback.get_feedback(feedback_id)
        # form=FeedbackForm(obj=f)
        Feedback.delete_feedback(feedback_id)
        flash('Feedback deleted')
    else:
        flash('Not allowed to delete')
    return redirect(f'/users/{username}')
    