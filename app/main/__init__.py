from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from config import config_by_name
from flask.app import Flask
from flask_jwt_extended import JWTManager
from flask_mail import Mail

db = SQLAlchemy()
flask_bcrypt = Bcrypt()
jwt = JWTManager()
mail = Mail()


def create_app(config_name: str) -> Flask:
#     app = Flask(__name__, static_folder="E:\\Users\\Anyone\\Desktop\\dev_phishing system\\app\\main\\static",
        #     static_url_path="")
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    return app
