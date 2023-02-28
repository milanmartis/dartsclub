from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import os
from dotenv import load_dotenv
import string
import random
# letters = string.ascii_lowercase
# my_secret_key = ( ''.join(random.choice(letters) for i in range(10)) )
load_dotenv()


db = SQLAlchemy()


DB_NAME = "../instance/"



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "dgskfgaksjfgajhdgasjhgajhdgajdgajhsdasjdaayiausyiausdiauyaisuyaizxzxzxc1233xxc"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://poktwcytjzkyew:5bdb99586baef51b1216188e45bb88c9e1af011a78e3a6d609e4938c2f60002a@ec2-52-23-81-126.compute-1.amazonaws.com:5432/db3uoc7j05udub'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(DB_NAME, 'database.db')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    # app.app_context().push()

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note, Groupz, Duel

    app.app_context().push()
    db.create_all()

    login_manager = LoginManager()
    login_manager.session_protection = "strong"
    login_manager.init_app(app)
    login_manager.login_view = '/login'
    
    
    # user_email = session.get('user_email')


    @login_manager.user_loader
    def load_user(id):
        try:
            return User.query.get(id)
        except:
            return None
        
    return app

# def create_database(app):
#     if not path.exists(DB_NAME):
#         with app.app_context():
#             db.create_all()
#         print('Created Database!')

create_app()