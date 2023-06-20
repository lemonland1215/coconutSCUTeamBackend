from flask import request
from app.main import db, scheduler
# from app.main.model.task import Task
from app.main.model.user import User
from app.main.model.project import Project
from app.main.model.server_catcher import Servercatcher
# from app.main.model.server_sender import Serversender
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
def save_new_catcher(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    catcher = Servercatcher.query.filter_by(name=data['name']).first()
    if not catcher:
        new_catcher = Servercatcher()
        data = request.json
        print("ok here")
        wj2o(new_catcher, data)
        save_changes(new_catcher)
        return response_with(SUCCESS_201)
    else:
        response_object = {
            'status': 'fail',
            'message': 'server sender already exists.',
        }
        return response_object, 409

def get_a_catcher(id):
    return Servercatcher.query.filter_by(id=id).first(), 201

def get_all_catchers():
    return Servercatcher.query.all(), 201


@jwt_required()
def update_a_catcher(id):
    # update task info ,status not included
    tmp_catcher = Servercatcher.query.filter_by(id=id).first()
    if not tmp_catcher:
        return response_with(ITEM_NOT_EXISTS)
    if tmp_catcher.islocked == True:
        return response_with(ITEM_LOCKED_400)
    update_val = request.json
    update_val['modifiedbyuid'] = get_jwt_identity()
    update_val['modifytime'] = datetime.now()
    wj2o(tmp_catcher, update_val)

    save_changes(tmp_catcher)
    response_object = {
        'code': 'success',
        'message': f'server catcher {id} updated!'.format()
    }
    return response_object, 201

@jwt_required()
def operate_a_catcher(id, operator):
    tmp_catcher = Servercatcher.query.filter_by(id=id).first()

    if not tmp_catcher:
        return response_with(ITEM_NOT_EXISTS)
    if tmp_catcher.islocked:
        if operator != "unlock":
            print('已经上锁了，请先解锁')
            return {
               "code": "locked",
               "message": "locked, please unlock first."
            }, 400
        else:
            tmp_catcher.islocked = False
            tmp_catcher.locktime = None
            tmp_catcher.lockbyuid = None
    else:
        if operator == "lock":
            tmp_catcher.islocked = True
            tmp_catcher.locktime = datetime.now()
            tmp_catcher.lockbyuid = get_jwt_identity()
        elif operator == "delete":
            db.session.delete(tmp_catcher)
            for sender in Servercatcher.query.filter_by(id=id).all():
                operate_a_catcher(sender.id, "delete")
        elif operator == "freeze":
            tmp_catcher.isfrozen = True
            tmp_catcher.freezetime = datetime.now()
            tmp_catcher.frozenbyuid = get_jwt_identity()
        elif operator == "unfreeze":
            tmp_catcher.isfrozen = False
            tmp_catcher.freezetime = None
            tmp_catcher.frozenbyuid = None
        elif operator == "open":
            if tmp_catcher.status != 'close':
                return response_with(ITEM_STATUS_400)
            else:
                tmp_catcher.status = 'open'
        elif operator == "close":
            if tmp_catcher.status != 'open':
                return response_with(ITEM_STATUS_400)
            else:
                tmp_catcher.status = 'close'
        else:
            print("有问题，你再看看你的操作呢")
            return response_with(INVALID_INPUT_422)
    db.session.commit()
    print("?")
    return response_with(SUCCESS_201)

def search_for_catchers(data):
    # name|server|port|encryptalg|isfrozen|islocked
    tmp_catchers = Servercatcher.query
    # tmp_projects = Project.query
    try:
        if data['name']:
            tmp_catchers = tmp_catchers.filter(Servercatcher.name.like("%" + data['name'] + "%"))
    except:
        print("no name")

    try:
        if data['server']:
            tmp_catchers = tmp_catchers.filter(Servercatcher.server.like("%" + data['server'] + "%"))
    except:
        print("no server")

    try:
        if data['port']:
            tmp_catchers = tmp_catchers.filter_by(port=data['port'])
    except:
        print("no port")

    try:
        if data['isfrozen']:
            tmp_catchers = tmp_catchers.filter_by(isfrozen=data['isfrozen'])
    except:
        print("no isfrozen")

    try:
        if data['islocked']:
            tmp_catchers = tmp_catchers.filter_by(islocked=data['islocked'])
    except:
        print("no isfrozen")

    # print(tmp_tasks.all())
    # print(tmp_projects.all())
    return tmp_catchers.all(), 201

def save_changes(data: Servercatcher) -> None:
    db.session.add(data)
    db.session.commit()