from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db=SQLAlchemy()

bcrypt=Bcrypt()
def connect_db(app):
    db.app=app
    db.init_app(app)
    app.app_context().push()

class User(db.Model):
    __tablename__='users'
    def __repr__(self):
        return f"<username={self.username}, password{self.password}, email={self.email}, first_name={self.first_name},last_name={self.last_name}>"
    
    username= db.Column(db.String(20),
                  primary_key=True, unique=True)
    password=db.Column(db.Text,
                   nullable=False)
    email=db.Column(db.String(50),
                      nullable=False, unique=True)
    first_name=db.Column(db.Text, nullable=False)
    last_name=db.Column(db.Text, nullable=False)
    password_reset_token=db.Column(db.Text)
    
    feedback=db.relationship('Feedback',
                             back_populates="author",
                             cascade="save-update, merge, delete")
   
    @classmethod
    def register(cls, user):
        if cls.__check_existence(user):
            hashed=bcrypt.generate_password_hash(user['password'])
            hashed_utf8=hashed.decode("utf8")
            
            new_user= cls(username=user['username'],
                        password=hashed_utf8,
                        email=user['email'],
                        first_name=user['first_name'],
                        last_name=user['last_name'])
            db.session.add(new_user)   
            db.session.commit()
            return new_user
        return False
    
    def __check_existence(user):
        u=User.query.filter_by(email=user['email']).first()
        if not u:
            u=User.query.filter_by(username=user['username']).first()
            if not u:
                return True
        return False
    
    @classmethod
    def login(cls, username,pwd):
        u=cls.query.filter_by(username=username).first()
        if u and bcrypt.check_password_hash(u.password,pwd):
            return u
        else:
            return False
    
    @classmethod
    def get_user(cls, username):
        u=cls.query.filter_by(username=username).first()
        return u
    
    @classmethod
    def delete_user(cls, username):
        u=cls.query.filter_by(username=username).first()
        db.session.delete(u)
        db.session.commit()
        return True
        

class Feedback(db.Model):
    __tablename__='feedback'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.Text,nullable=False)
    content=db.Column(db.Text,nullable=False)
    username=db.Column(db.Text,db.ForeignKey('users.username'),nullable=False)
    
    author = db.relationship(
        'User',
        back_populates='feedback')
    
    @classmethod
    def add_feedback(cls,username,title,content):
        try:
            f= cls(title=title,content=content,username=username)
            db.session.add(f)
            db.session.commit()
            return True
        except Exception as e:
            return e
    
    @classmethod
    def get_feedback(cls,feedback_id):
        f=cls.query.get_or_404(feedback_id)
        return f 

    @classmethod
    def update_feedback(cls,feedback_id, title, content):
        f=cls.query.get_or_404(feedback_id)
        f.title=title
        f.content=content
        db.session.add(f)
        db.session.commit()
        return f 
    
    @classmethod
    def delete_feedback(cls,feedback_id):
        f=cls.query.get_or_404(feedback_id)
        db.session.delete(f)
        db.session.commit()