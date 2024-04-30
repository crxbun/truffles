from truffles import db
from sqlalchemy import Integer, VARCHAR, Text, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import mapped_column
import datetime

class User(db.Model):
        __tablename__ = 'user'
        id = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
        username = mapped_column(VARCHAR(200), unique=True, nullable=False)
        password = mapped_column(Integer, nullable=False)

class Truffle(db.Model):
        __tablename__ = 'truffle'
        id = mapped_column(Integer, autoincrement=True, unique=True, primary_key=True)
        name = mapped_column(VARCHAR(200), unique=True, nullable=False)
        age = mapped_column(Integer, nullable=False)
        status = mapped_column(Integer, nullable=False)

class UserTruffle(db.Model):
        __tablename__ = 'user_truffle'
        id = mapped_column(Integer, autoincrement=True, unique=True, nullable=False, primary_key=True)
        userID = mapped_column(ForeignKey('user.id'), nullable=False)
        truffleID = mapped_column(ForeignKey('truffle.id'), nullable=False)

class TruffleAccessories(db.Model):
        __tablename__= 'truffle_accessories'
        id = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
        truffleID = mapped_column(ForeignKey('user.id'))
        headwear = mapped_column(VARCHAR(300), nullable=True)

class Chatroom(db.Model):
        __tablename__ = 'chatroom'
        id = mapped_column(Integer, unique=True, primary_key=True, autoincrement=True)
        message = mapped_column(Text, nullable=False)
        userID = mapped_column(ForeignKey('user.id'), nullable=False)

class Messages(db.Model):
        __tablename__ = 'messages'
        id = mapped_column(Integer, primary_key=True, autoincrement=True)
        chatroomID = mapped_column(ForeignKey('chatroom.id'), nullable=False)
        senderID = mapped_column(ForeignKey('user.id'), nullable=False)
        body = mapped_column(Text, nullable=False)
        read = mapped_column(Boolean, nullable=False, default=False)
        timestamp = mapped_column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

class Participants(db.Model):
        __tablename__= 'participants'
        id = mapped_column(Integer, unique=True, primary_key=True, autoincrement=True)
        chatroomID = mapped_column(ForeignKey('chatroom.id'), nullable=False)
        userID = mapped_column(ForeignKey('user.id'), nullable=False)