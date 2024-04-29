from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
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
db = SQLAlchemy(app)


#class Base(DeclarativeBase):
 #   pass

#db =SQLAlchemy(app, model_class=Base)

# from truffles.models import ... import models here

with app.app_context():
    db.create_all()