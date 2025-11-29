from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.theme import Bootstrap4Theme

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.signin'

admin = Admin(name='Cafe Administration', theme=Bootstrap4Theme(swatch='cerulean'))
