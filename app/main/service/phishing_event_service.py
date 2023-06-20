from flask import request
from app.main import db, scheduler
from app.main.model.phishing_event import Phishingevent
from typing import Dict, Tuple
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.main.util.write_json_to_obj import wj2o
from datetime import datetime
from app.main.util.response_tip import *
from flask_mail import Mail, Message
from extention import app
import json
from app.main.service.log_service import save_log

running_jobs = {}

def get_a_event(id):
    return Phishingevent.query.filter_by(id=id).first(), 201

def get_all_events():
    return Phishingevent.query.all(), 201

def save_new_event(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    new_event = Phishingevent()
    # data = request.json
    data['time'] = datetime.now()
    wj2o(new_event, data)
    save_changes(new_event)
    details = " save a new event."
    save_log("Create", get_jwt_identity(), details)
    return response_with(SUCCESS_201)

@jwt_required()
def search_for_events(data):
    tmp_events = Phishingevent.query
    try:
        if data['uid']:
            print(data['uid'])
            tmp_events = tmp_events.filter_by(uid=data['uid'])
    except:
        print("或许这是鄙人的问题，但我们的确没有找到这位用户相关的记录")

    try:
        if data['catcher_id']:
            tmp_events = tmp_events.filter_by(catcher_id=data['catcher_id'])
    except:
        print("没有，没有，这里没有这个捕获服务器相关的记录，没有...")

    try:
        if data['task_id']:
            tmp_events = tmp_events.filter_by(task_id=data['task_id'])
    except:
        print("找啊找，没有这个task相关的内容哦，算不算是另类的欧气呢？")

    try:
        if data['server_id']:
            tmp_events = tmp_events.filter_by(server_id=data['server_id'])
    except:
        print("ERROR发生，没有找到该发送方服务器相关的信息（冰冷的机械音）")

    return tmp_events.all(), 201

def save_changes(data: Phishingevent) -> None:
    db.session.add(data)
    db.session.commit()