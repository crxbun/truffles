from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import os

static_folder = 'static'

app = Flask(__name__)
base_path = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(base_path, "truffles.db") # change to mysql path
app.secret_key = "placeholder"

class Base(DeclarativeBase):
    pass

db =SQLAlchemy(app, model_class=Base)

# from truffles.models import ... import models here

with app.app_context():
    db.create_all()