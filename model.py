from app import db
import datetime

followers = db.Table('followers',
                      db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                      db.Column('followed_id', db.Integer, db.ForeignKey('user.id')))


class User (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    followed = db.relationship('User',
                                secondary=followers,
                                primaryjoin=(followers.c.follower_id == id),
                                secondaryjoin=(followers.c.followed_id == id),
                                backref=db.backref('followers', lazy='dynamic'),
                                lazy='dynamic')


class Message (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey ('user.id'))
    user = db.relationship('User', backref='message')
    message_text = db.Column(db.String)
    date_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)