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

running_jobs = {}

def get_a_event(id):
    return Phishingevent.query.filter_by(id=id).first(), 201

def get_all_events():
    return Phishingevent.query.all(), 201

@jwt_required()
def search_for_events(data):
    # 编号、名称、创建日期、修改日期、项目id、项目名称、项目经理id、冻结状态
    tmp_events = Phishingevent.query
    try:
        if data['uid']:
            print(data['uid'])
            tmp_events = tmp_events.filter_by(uid=data['uid'])
    except:
        print("非常抱歉，不过我们这儿似乎没有相关用户的记录")

    try:
        if data['uname']:
            tmp_events = tmp_events.filter(Phishingevent.uname.like("%" + data['uname'] + "%"))
    except:
        print("或许这是鄙人的问题，但我们的确没有找到这位用户相关的记录")

    try:
        if data['task_id']:
            tmp_events = tmp_events.filter_by(task_id=data['task_id'])
    except:
        print("这是属下的失职！但是确实没有发现这个评测任务相关的中招记录！")

    try:
        if data['catcher_id']:
            tmp_events = tmp_events.filter_by(catcher_id=data['catcher_id'])
    except:
        print("没有，没有，这里没有这个捕获服务器相关的记录，没有...")

    try:
        if data['server_id']:
            tmp_events = tmp_events.filter_by(server_id=data['server_id'])
    except:
        print("ERROR发生，没有找到该发送方服务器相关的信息（冰冷的机械音）")

    return tmp_events.all(), 201