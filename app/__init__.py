from flask_restx import Api
from flask import Blueprint

from .main.controller.organization_controller import ns as organization_ns
from .main.controller.user_controller import ns as user_ns
from .main.controller.auth_controller import ns as auth_ns

api_blueprint = Blueprint('flask-restx', __name__)
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    api_blueprint,
    title='PHISHING SYS',
    version='1.0',
    description="a phishing system's api",
    authorizations=authorizations,
    security='apikey'
)

api.add_namespace(organization_ns, path='/organization')
api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns, path='/auth')
