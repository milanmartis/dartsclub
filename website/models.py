from website import db
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import PrimaryKeyConstraint
from flask import current_app





user_duel = db.Table('user_duel',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id', onupdate="CASCADE", ondelete="CASCADE")),
                     db.Column('duel_id', db.Integer, db.ForeignKey('duel.id', onupdate="CASCADE", ondelete="CASCADE")),
                     db.Column('result', db.Integer, default=0),
                     db.Column('against', db.Integer, default=0),
                     db.Column('points', db.Integer, default=0),
                     db.Column('checked', db.String(10), default="false"),
                     db.Column('notez', db.Integer),
                     db.Column('addons', db.Integer, default=1)
                     )

user_group = db.Table('user_group',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('groupz_id', db.Integer, db.ForeignKey('groupz.id')),
                     db.Column('season_id', db.Integer, db.ForeignKey('season.id')),
                     db.Column('round_id', db.Integer, db.ForeignKey('round.id'))
                     )

user_season = db.Table('user_season',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('season_id', db.Integer, db.ForeignKey('season.id')),
                     db.Column('season_first_date', db.DateTime(timezone=True), default=func.now()),
                     db.Column('orderz', db.Integer)
                     )




# class Role(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200))
#     date = db.Column(db.DateTime(timezone=True), default=func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# class Facility(db.Model):
#     id = db.Column(db.Integer, primary_key=True)




class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.String(10000))
    date_time = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Groupz(db.Model):
    __tablename__ = 'groupz'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(300))
    shorts = db.Column(db.Text)
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'))
    round_id = db.Column(db.Integer, db.ForeignKey('round.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

    orderz = db.Column(db.Integer)
    notes = db.relationship('Note')
    seasony = db.relationship('Season', secondary=user_season, backref='seasons')
    groupy = db.relationship('Groupz', secondary=user_group, backref='groups')
    play = db.relationship('Duel', secondary=user_duel, backref='players')
    # public_id = db.Column(db.Integer)
    authenticated = db.Column(db.Boolean, default=False)
    confirm = db.Column(db.Boolean, default=False)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def is_admin(self):
        return self.admin

    def get_id(self):
        return self.id


    def get_reset_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    def get_confirm_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(int(user_id))

    @staticmethod
    def verify_confirm_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(int(user_id))

class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'))


class Season(db.Model):
    __tablename__ = 'season'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    
    season_from = db.Column(db.DateTime(timezone=True), default=func.now())
    season_to = db.Column(db.DateTime(timezone=True), default=func.now())
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Duel(db.Model):
    __tablename__ = 'duel'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    notice = db.Column(db.String(10000))

    date_duel = db.Column(db.DateTime(timezone=True), default=func.now())
    openhour = db.relationship('OpenHour', backref='duel', uselist=False)
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'))
    round_id = db.Column(db.Integer, db.ForeignKey('round.id'))

# class PlayGround(db.Model):
# class Season(db.Model):


class OpenHour(db.Model):
    __tablename__ = 'openhour'
    id = db.Column(db.Integer, primary_key=True)
    notice = db.Column(db.String(500))
    oh_from = db.Column(db.DateTime(timezone=True), default=func.now())
    oh_to = db.Column(db.DateTime(timezone=True), default=func.now())
    duel_id = db.Column(db.Integer, db.ForeignKey('duel.id'))



class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    stripe_link = db.Column(db.String(100), nullable=False)
    youtube_link = db.Column(db.String(300), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=func.now())
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_visible = db.Column(db.Boolean(), default=True)
    price = db.Column(db.DECIMAL(precision=10, scale=2), nullable=False)
    old_price = db.Column(db.DECIMAL(precision=10, scale=2), nullable=False)
    product_category_id = db.Column(db.Integer, db.ForeignKey(
        'product_category.id'), nullable=False)
    product_gallery = db.relationship('ProductGallery', backref='gallpr', lazy=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}', '{self.product_gallery}, '{self.product_category_id}')"


class ProductCategory(db.Model):
    __tablename__ = 'product_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    
    
class ProductGallery(db.Model):
    __tablename__ = 'product_gallery'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image_file2 = db.Column(db.String(30), nullable=False)
    # image_order = db.Column(db.Integer, unique=True, nullable=False)
    orderz = db.Column(db.Integer)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
