from flask import request
from app.main import db, scheduler
# from app.main.model.task import Task
from app.main.model.user import User
from app.main.model.project import Project
from app.main.model.server_catcher import Servercatcher
from app.main.model.server_sender import Serversender
from app.main.model.mail_template import Mailtemplate
from typing import Dict, Tuple
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.main.util.write_json_to_obj import wj2o
from datetime import datetime
from app.main.util.response_tip import *
from flask_mail import Mail, Message
from extention import app
import json


running_jobs = {}

@jwt_required()
def save_new_sender(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    sender = Servercatcher.query.filter_by(name=data['name']).first()
    if not sender:
        new_sender = Servercatcher()
        data = request.json
        data['createdbyuid'] = get_jwt_identity()
        wj2o(new_sender, data)
        save_changes(new_sender)
        return response_with(SUCCESS_201)
    else:
        response_object = {
            'status': 'fail',
            'message': 'server sender already exists.',
        }
        return response_object, 409

def get_a_sender(id):
    return Servercatcher.query.filter_by(id=id).first(), 201

def get_all_senders():
    return Servercatcher.query.all(), 201

@jwt_required()
def update_a_sender(id):
    # update task info ,status not included
    tmp_sender = Serversender.query.filter_by(id=id).first()
    if not tmp_sender:
        return response_with(ITEM_NOT_EXISTS)
    if tmp_sender.islocked == True:
        return response_with(ITEM_LOCKED_400)
    update_val = request.json
    update_val['modifiedbyuid'] = get_jwt_identity()
    update_val['modifytime'] = datetime.now()
    wj2o(tmp_sender, update_val)

    save_changes(tmp_sender)
    response_object = {
        'code': 'success',
        'message': f'server sender {id} updated!'.format()
    }
    return response_object, 201

@jwt_required()
def operate_a_sender(id, operator):
    tmp_sender = Serversender.query.filter_by(id=id).first()

    if not tmp_sender:
        return response_with(ITEM_NOT_EXISTS)
    if tmp_sender.islocked:
        if operator != "unlock":
            print('已经上锁了，请先解锁')
            return response_with(ITEM_LOCKED_400)
        else:
            tmp_sender.islocked = False
    else:
        if operator == "lock":
            tmp_sender.islocked = True
        elif operator == "delete":
            db.session.delete(tmp_sender)
            for sender in Serversender.query.filter_by(id=id).all():
                operate_a_sender(sender.id, "delete")
        elif operator == "freeze":
            tmp_sender.isfrozen = True
            tmp_sender.freezetime = datetime.now()
            tmp_sender.frozenbyuid = get_jwt_identity()
        elif operator == "unfreeze":
            tmp_sender.isfrozen = False
            tmp_sender.freezetime = None
            tmp_sender.frozenbyuid = None
        else:
            print("有问题，你再看看你的操作呢")
            return response_with(INVALID_INPUT_422)
    db.session.commit()
    return response_with(SUCCESS_201)


def save_changes(data: Servercatcher) -> None:
    db.session.add(data)
    db.session.commit()