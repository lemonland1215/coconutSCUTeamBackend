from app.main.model.log import Log
from app.main.model.user import User
from app.main.model.organization import Organization
from app.main.model.project import Project
from app.main.model.task import Task
from app.main.model.phishing_event import Phishingevent


def get_statistics():
    response_object = {
        'code': 'success',
        'user number': User.query.count(),
        'organization number': Organization.query.count(),
        'project number': Project.query.count(),
        'task number': Task.query.count(),
        'event number': Phishingevent.query.count(),
        'log number': Log.query.count()
    }
    return response_object, 200
