from flask import request
from app.main import db
from app.main.model.log import Log
from app.main.model.user import User
from app.main.model.liaison import Liaison
from app.main.model.organization import Organization
from typing import Dict, Tuple
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.main.util.write_json_to_obj import wj2o
from datetime import datetime


def get_all_logs():
    tmp_log = db.session.query(Log.id, Log.type, Log.operator_id, User.username.label('operator'), Log.role, Log.details,
                         Log.time).\
        outerjoin(User, Log.operator_id == User.id)
    return tmp_log.all()


def save_log(type, userid, description):
    login = Log()
    login.type = type
    login.operator_id = userid
    login.role = list(db.session.query(User.sysrole).filter(User.id == userid).first())[0]
    login.details = list(db.session.query(User.username).filter(User.id == userid).first())[0] + description
    login.time = datetime.now()
    db.session.add(login)
    db.session.commit()
