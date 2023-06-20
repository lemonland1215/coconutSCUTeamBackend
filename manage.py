import os
import unittest
from app.main import db, jwt
from app import api_blueprint
from app.main.model.user import User
from app.main.model.mail_template import Mailtemplate
from app.main.model.auth import TokenBlocklist
from flask import Response, render_template
from flask.cli import FlaskGroup
from extention import app, app_catcher

from app.main.model.organization import Organization
from app.main.model.project import Project
from app.main.model.task import Task
from app.main.model.server_catcher import Servercatcher
from app.main.model.server_sender import Serversender
from app.main.model.log import Log
from app.main.model.phishing_event import Phishingevent



app.register_blueprint(api_blueprint)
app.app_context().push()

cli = FlaskGroup('phishingtest')
cli.add_command("run", app)
cli.add_command("run_catcher", app_catcher)


@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response




@app_catcher.cli.command("run_catcher")
def run_catcher():
    app_catcher.run(host='0.0.0.0', port=6000)

@app.cli.command("run")
def run():
    app.run(host="127.0.0.1")



@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None


@app.route("/init_db")
def create():
    db.drop_all()
    db.create_all()
    User.init_db()
    Mailtemplate.init_db()
    Organization.init_db()
    Project.init_db()
    Task.init_db()
    Servercatcher.init_db()
    Serversender.init_db()
    return "db inited"

@app_catcher.route("/")
def index():
    return render_template("dy.html")


if __name__ == '__main__':
    # cli()
#     cli = FlaskGroup(app_catcher)
#     print(cli.commands)

    app.run(host='0.0.0.0', port=5000)
    # app_catcher.run(host='0.0.0.0', port=6000)

