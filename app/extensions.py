from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.theme import Bootstrap4Theme
from redis import Redis

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.signin'

redis_client = Redis(
    host='localhost', port=6379, db=0, decode_responses=True
)

admin = Admin(name='Cafe Administration', theme=Bootstrap4Theme())
