from truffles import db
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
import datetime

class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(200), unique=True, nullable=False)
    #password = Column(String, nullable=False)
    # Define relationship with Messages
    messages = relationship('Messages', backref='sender', lazy=True)

class Truffle(db.Model):
    __tablename__ = 'truffle'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)

class UserTruffle(db.Model):
    __tablename__ = 'user_truffle'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    truffle_id = Column(Integer, ForeignKey('truffle.id'), nullable=False)

class TruffleAccessories(db.Model):
    __tablename__= 'truffle_accessories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    truffle_id = Column(Integer, ForeignKey('truffle.id'), nullable=False)
    headwear = Column(String(300), nullable=True)

class Chatroom(db.Model):
    __tablename__ = 'chatroom'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(200), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    participants_count = Column(Integer, default=0, nullable=False)
    # Define relationship with Messages
    messages = relationship('Messages', backref='chatroom', lazy=True)

class Messages(db.Model):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    chatroom_code = Column(String(200), ForeignKey('chatroom.code'), nullable=False)
    sender_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    body = Column(Text, nullable=False)
    read = Column(Boolean, nullable=False, default=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class Participants(db.Model):
    __tablename__= 'participants'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(200), ForeignKey('chatroom.code'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

class UserChatroom(db.Model):
    __tablename__='user_chatroom'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(200), ForeignKey('chatroom.code'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
