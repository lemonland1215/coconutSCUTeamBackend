from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_apscheduler import APScheduler

from config import config_by_name
from flask.app import Flask
from flask_jwt_extended import JWTManager
from flask_mail import Mail

db = SQLAlchemy()
flask_bcrypt = Bcrypt()
jwt = JWTManager()
mail = Mail()
scheduler = APScheduler()

def create_app(config_name: str) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    app.config['JWT_SECRET_KEY'] = 'key_for_test'
    db.init_app(app)
    flask_bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    scheduler.init_app(app)
    scheduler.start()

    return app

def create_catcher_app():
    app = Flask(__name__,
            # static_url_path = 'catcher', # 配置静态文件的访问 url 前缀
            # static_folder = os.path.join(BASE_DIR, 'static'),    # 配置静态文件的文件夹
            # template_folder = os.path.join(BASE_DIR, 'templates') # 配置模板文件的文件夹
            )
    return app
