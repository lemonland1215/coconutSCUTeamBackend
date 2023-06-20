from flask_restx import Api
from flask import Blueprint

from .main.controller.organization_controller import ns as organization_ns
from .main.controller.user_controller import ns as user_ns
from .main.controller.auth_controller import ns as auth_ns
from .main.controller.project_controller import ns as project_ns
from .main.controller.task_controller import ns as task_ns
from .main.controller.mail_controller import ns as mail_ns
from .main.controller.file_controller import ns as file_ns
from .main.controller.log_controller import ns as log_ns
from .main.controller.sender_controller import ns as sender_ns
from .main.controller.phishing_event_controller import ns as event_ns
from .main.controller.catcher_controller import ns as catcher_ns
from .main.controller.qr_controller import ns as qr_ns


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
api.add_namespace(project_ns, path='/project')
api.add_namespace(task_ns, path='/task')
api.add_namespace(mail_ns, path='/mail')
api.add_namespace(file_ns, path='/upload')
api.add_namespace(log_ns, path='/log')
api.add_namespace(sender_ns, path='/sever_sender')
api.add_namespace(event_ns, path='/phishing_event')
api.add_namespace(catcher_ns, path='/server_catcher')
api.add_namespace(qr_ns, path='/qrcode')

