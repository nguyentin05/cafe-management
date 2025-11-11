import os

from cloudinary.utils import cloudinary_url
from flask import Flask
from dotenv import load_dotenv
from flask_admin.theme import Bootstrap4Theme
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
import cloudinary

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"]=3

admin = Admin(app=app, name='Cafe Administration', theme=Bootstrap4Theme(swatch='cerulean'))

login = LoginManager(app=app)

db = SQLAlchemy(app=app)

cloudinary.config(cloudinary_url=os.getenv('CLOUDINARY_URL'), secure=True)