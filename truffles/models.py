from sqlalchemy import Integer, VARCHAR, Text, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import mapped_column
import datetime

def define_models(db):
    class User(db.Model):
        __tablename__ = 'user'
        id = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
        username = mapped_column(VARCHAR(255), unique=True, nullable=False)
        password = mapped_column(Integer, nullable=False)

    class Truffle(db.Model):
        __tablename__ = 'truffle'
        id = mapped_column(Integer, autoincrement=True, unique=True, primary_key=True)
        name = mapped_column(VARCHAR(255), unique=True, nullable=False)
        age = mapped_column(Integer, nullable=False)
        status = mapped_column(Integer, nullable=False)

    class UserTruffle(db.Model):
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        __tablename__ = 'user_truffle'
        userID = mapped_column(ForeignKey('user.id'), nullable=False)
        truffleID = mapped_column(ForeignKey('truffle.id'), nullable=False)

    class TruffleAccessories(db.Model):
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        truffleID = mapped_column(ForeignKey('user.id'))
        headwear = mapped_column(VARCHAR(255), nullable=True)

    class Chatroom(db.Model):
        __tablename__ = 'chatroom'
        id = mapped_column(Integer, unique=True, primary_key=True)
        message = mapped_column(VARCHAR(255), nullable=False)
        userID = mapped_column(ForeignKey('user.id'), nullable=False)

    class Messages(db.Model):
        __tablename__ = 's'
        id = mapped_column(Integer, primary_key=True)
        chatroomID = mapped_column(ForeignKey('chatroom.id'), nullable=False)
        senderID = mapped_column(ForeignKey('user.id'), nullable=False)
        body = mapped_column(Text, nullable=False)
        read = mapped_column(Boolean, nullable=False, default=False)
        timestamp = mapped_column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    class Participants(db.Model):
        __tablename__= 'participants'
        id = mapped_column(Integer, unique=True, primary_key=True)
        chatroomID = mapped_column(ForeignKey('chatroom.id'), nullable=False)
        userID = mapped_column(ForeignKey('user.id'), nullable=False)
    return User, Truffle, UserTruffle, TruffleAccessories, Chatroom, Messages, Participants
    