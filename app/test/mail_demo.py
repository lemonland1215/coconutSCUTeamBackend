from flask import Flask
from flask_mail import Mail, Message
import os
from configures.development import QqMailConfig, MsMailConfig



class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'sdfghsdf#$%&#@#$')


class QMailConfig(BaseConfig):
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'xx@qq.com'
    MAIL_PASSWORD = 'xxxxxxxx'
    MAIL_DEFAULT_SENDER="xxx@qq.com"
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False

mail = Mail()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)
    return app

app = create_app(QMailConfig)

@app.route("/")
def index():
    return "mail sender demo"


@app.route("/sendbyqq")
def sendbyqq():
    app.config.from_object(QqMailConfig)
    mail.init_app(app)
    msg = Message("qqHello", recipients=["winshine_new@qq.com"])
    msg.body = "Hello Flask message sent from Flask-Mail"
    mail.send(msg)
    return "from qq, sent!"

@app.route("/sendbyms")
def sendbyms():
    app.config.from_object(MsMailConfig)
    mail.init_app(app)
    msg = Message("msHello", recipients=["winshine_new@qq.com"])
    msg.body = "Hello Flask message sent from Flask-Mail"
    mail.send(msg)
    return "from ms, sent!"


app.run(debug=True)
