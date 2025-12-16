import os

from cloudinary.utils import cloudinary_url
from flask import Flask, session

from .daos.order_dao import get_value
from .extensions import db, login, admin as admin_ext, redis_client

from dotenv import load_dotenv
import cloudinary

from .daos.dish_dao import load_dish_categories, load_category_groups
from .utils import get_total_session

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.secret_key = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config["PAGE_SIZE"] = 3


    app.config["MOMO_PARTNER_CODE"] = os.getenv("MOMO_PARTNER_CODE")
    app.config["MOMO_ACCESS_KEY"] = os.getenv("MOMO_ACCESS_KEY")
    app.config["MOMO_SECRET_KEY"] = os.getenv("MOMO_SECRET_KEY")
    app.config["MOMO_ENDPOINT"] = os.getenv("MOMO_ENDPOINT")
    app.config["MOMO_REDIRECT_URL"] = os.getenv("MOMO_REDIRECT_URL")
    app.config["MOMO_IPN_URL"] = os.getenv("MOMO_IPN_URL")
    app.config["MOMO_REQUEST_TYPE"] = os.getenv("MOMO_REQUEST_TYPE")

    from .models.order import RegulationKey

    @app.context_processor
    def common_attributes():
        return {
            'dish_categories': load_dish_categories(),
            'category_groups': load_category_groups(),
            'cart_stats': get_total_session(session.get('cart')),
            'service_fee': float(get_value(key=RegulationKey.SERVICE_FEE_PERCENT)),
            'min_ingredient': int(get_value(key=RegulationKey.MIN_INGREDIENT))
        }

    login.init_app(app)
    db.init_app(app)
    admin_ext.init_app(app)

    from app import models
    from app import admin as admin_module
    admin_module.init_admin(admin_ext)

    from .controllers.auth_controller import auth
    from .controllers.api_customer_controller import api_customer
    from .controllers.api_employee_controller import api_employee
    from .controllers.customer_controller import customer
    from .controllers.employee_controller import employee
    from .controllers.main_controller import main
    from .controllers.waiter_controller import waiter
    from .controllers.manager_controller import manager

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(api_customer, url_prefix='/api/customer')
    app.register_blueprint(api_employee, url_prefix='/api/employee')
    app.register_blueprint(customer, url_prefix='/customer')
    app.register_blueprint(employee, url_prefix='/employee')
    app.register_blueprint(main)
    app.register_blueprint(waiter, url_prefix='/waiter')
    app.register_blueprint(manager, url_prefix='/manager')

    cloudinary.config(cloudinary_url=os.getenv('CLOUDINARY_URL'), secure=True)

    return app