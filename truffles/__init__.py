from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import inspect
import os
import sshtunnel

static_folder = 'static'

app = Flask(__name__)

if __name__ == '__main__':
    tunnel = sshtunnel.SSHTunnelForwarder(
        ('ssh.pythonanywhere.com'),
        ssh_username='LolOreoGod', ssh_password='SSHPassword!',
        remote_bind_address=('LolOreoGod.mysql.pythonanywhere-services.com', 3306)
    )

    tunnel.start()

    #base_path = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://LolOreoGod:123456qwerty!@127.0.0.1:{}/LolOreoGod$truffledb".format(tunnel.local_bind_port)
#app.secret_key = "placeholder"

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(app, model_class=Base) 


#class Base(DeclarativeBase):
 #   pass

# class Truffle(db.Model):
#     truffleID = db.Column(db.Integer, unique = True, primary_key = True)
#     truffleName = db.Column(db.String(100), nullable = False)


#db =SQLAlchemy(app, mod                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           el_class=Base)

from models import define_models

User, Truffle, UserTruffle, TruffleAccessories, Chatroom, Messages, Participants = define_models(db)

with app.app_context():
    db.create_all()
    # inspector = inspect(db.engine)
    # if inspector.has_table('truffle'):
    #     # Drop the table
    #     Truffle.__table__.drop(db.engine)
    