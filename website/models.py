from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import PrimaryKeyConstraint





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
