from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()
def connect_db(app):
    db.app=app
    db.init_app(app)
    app.app_context().push()


class User(db.Model):
    __tablename__='users'
    def __repr__(self):
        return f"<id={self.id}, name={self.name}, species{self.species}, photo_url={self.photo_url}, age={self.age},notes={self.notes},available={self.available}>"
    
    username= db.Column(db.String(20),
                  primary_key=True,
                  autoincrement=True)
    password=db.Column(db.Text,
                   nullable=False)
    email=db.Column(db.String(50),
                      nullable=False, unique=True)
    first_name=db.Column(db.Text, nullable=False)
    last_name=db.Column(db.Text, nullable=False)
   
