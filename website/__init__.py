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
    app.config['SECRET_KEY'] = "dgskfgaksjfgajhdgasjhgajhdgajdgajhsdasjdaayiausyiausdiauyaisuyaiusydiu"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ynqryzyuztgqts:122f26414b20598848fc10a2703fd6da06650c06918c1a69e5e7249d59597271@ec2-34-194-40-194.compute-1.amazonaws.com:5432/d8jkicn6gvjnuh'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(DB_NAME, 'database.db')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

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