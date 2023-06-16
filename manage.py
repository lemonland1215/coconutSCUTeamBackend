import os
import unittest
from flask_migrate import Migrate
from app import api_blueprint
from app.main import create_app, db, jwt
from app.main.model import organization, user
from app.main.model.auth import TokenBlocklist
from flask import Response

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.register_blueprint(api_blueprint)

app.app_context().push()
migrate = Migrate(app, db)


@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response


@app.cli.command("run")
def run():
    app.run(host="0.0.0.0")


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
    return "db inited"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5700)
