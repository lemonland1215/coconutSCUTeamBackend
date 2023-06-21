from app.main.model.log import Log
from app.main.model.user import User
from app.main.model.organization import Organization
from app.main.model.project import Project
from app.main.model.task import Task
from app.main.model.phishing_event import Phishingevent


def get_statistics():
    response_object = {
        'code': 'success',
        'user_number': User.query.count(),
        'organization_number': Organization.query.count(),
        'project_number': Project.query.count(),
        'task_number': Task.query.count(),
        'event_number': Phishingevent.query.count(),
        'log_number': Log.query.count()
    }
    return response_object, 200
