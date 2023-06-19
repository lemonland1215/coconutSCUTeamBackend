import os
import unittest
from app.main import db, jwt
from app import api_blueprint
from app.main.model.user import User
from app.main.model.liaison import Liaison
from app.main.model.mail_template import Mailtemplate
from app.main.model.auth import TokenBlocklist
from app.main.model.organization import Organization
from app.main.model.project import Project
from app.main.model.task import Task
from app.main.model.server_catcher import Servercatcher
from app.main.model.server_sender import Serversender
from flask import Response
from extention import app


app.register_blueprint(api_blueprint)

app.app_context().push()



@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response


@app.cli.command("run")
def run():
    app.run(host="127.0.0.1")


@app.cli.command("test")
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


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
    Liaison.init_db()
    Mailtemplate.init_db()
    Organization.init_db()
    Project.init_db()
    Task.init_db()
    Servercatcher.init_db()
    Serversender.init_db()
    return "db inited"


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000)

