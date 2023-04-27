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
# from flask_bcrypt import Bcrypt

db = SQLAlchemy()

DB_NAME = "../instance/"

login_manager = LoginManager()
login_manager.login_view = 'auth.login'



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(DB_NAME, 'database.db')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # bcrypt = Bcrypt(app)

    # app.app_context().push()
    login_manager.init_app(app)
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note, Groupz, Duel

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    return app


# def create_database(app):
#     if not path.exists(DB_NAME):
#         with app.app_context():
#             db.create_all()
#         print('Created Database!')

