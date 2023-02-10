from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import os

db = SQLAlchemy()


DB_NAME = "../instance/"



def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://sfljcgpqzpdtgy:e7cf417bcda516a158e6573deeef539aa5a8c641024736ae0dcad733e4116a82@ec2-54-173-77-184.compute-1.amazonaws.com:5432/d7lne9amqh2iri')
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(DB_NAME, 'database.db')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SECRET_KEY'] = 'secret'

    db.init_app(app)
    # app.app_context().push()

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note, Groupz, Duel

    app.app_context().push()
    # db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


   
    return app

# def create_database(app):
#     if not path.exists(DB_NAME):
#         with app.app_context():
#             db.create_all()
#         print('Created Database!')

create_app()