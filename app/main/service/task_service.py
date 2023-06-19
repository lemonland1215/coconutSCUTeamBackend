from flask import request
from app.main import db
from app.main.model.task import Task
from app.main.model.project import Project
from typing import Dict, Tuple
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.main.util.write_json_to_obj import wj2o
from datetime import datetime
from app.main.util.response_tip import *
from flask_mail import Mail, Message
import json


@jwt_required()
def save_new_task(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    task = Task.query.filter_by(name=data['name']).first()
    if not task:
        new_task = Task()
        data = request.json
        data['createdbyuid'] = get_jwt_identity()
        wj2o(new_task, data)
        save_changes(new_task)
        return response_with(SUCCESS_201)
    else:
        response_object = {
            'status': 'fail',
            'message': 'Task already exists.',
        }
        return response_object, 409


def get_a_task(id):
    return Task.query.filter_by(id=id).first(), 201


def get_all_tasks():
    return Task.query.all(), 201


def search_for_tasks(data):
    # 编号、名称、创建日期、修改日期、项目id、项目名称、项目经理id、冻结状态
    tmp_tasks = Task.query
    tmp_projects = Project.query

    try:
        if data['id']:
            print(data['id'])
            tmp_tasks = tmp_tasks.filter_by(id=data['id'])
    except:
        print("没有是这个编号的任务哦")

    try:
        if data['name']:
            tmp_tasks = tmp_tasks.filter(Task.name.like("%" + data['name'] + "%"))
    except:
        print("没有是这个名称的任务哦")

    try:
        if data['create_time_begin'] and data['create_time_end']:
            tmp_tasks = tmp_tasks.filter(
                Task.createtime.between(data['create_time_start'], data['create_time_end']))
            print(tmp_tasks.all())
    except Exception as e:
        print("没有在这个时间区间内创建的任务哦", e)

    try:
        if data['modify_time_start'] and data['modify_time_end']:
            tmp_tasks = tmp_tasks.filter(
                Task.modifytime.between(data['modify_time_start'], data['modify_time_end']))
    except:
        print("没有在这个时间区间修改的任务哦")

    try:
        if data['project_id']:
            tmp_tasks = tmp_tasks.filter_by(project_id=data['project_id'])
    except:
        print("没有是这个项目id的任务哦")

    try:
        if data['project_name']:
            print(data['project_name'])
            tmp_projects = tmp_projects.filter(Project.projectname.like("%" + data['project_name'] + "%")).all()
            print("hh")
            filtered_tasks = []  # 创建空的任务列表
            for tmp_project in tmp_projects:
                tmp_id = tmp_project.id
                tasks_for_project = tmp_tasks.filter_by(project_id=tmp_id).all()  # 获取每个项目的任务
                filtered_tasks.extend(tasks_for_project)  # 将每个项目的任务添加到任务列表中
            return filtered_tasks, 201  # 返回过滤后的任务列表
    except:
        print("没有是这个项目名称的任务哦")

    try:
        if data['project_manager_id']:
            print(data['project_manager_id'])
            tmp_projects = tmp_projects.filter_by(project_manager_id=data['project_manager_id']).all()
            filtered_tasks = []  # 创建空的任务列表
            for tmp_project in tmp_projects:
                tmp_id = tmp_project.id
                tasks_for_project = tmp_tasks.filter_by(project_id=tmp_id).all()  # 获取每个项目的任务
                filtered_tasks.extend(tasks_for_project)  # 将每个项目的任务添加到任务列表中
            return filtered_tasks, 201  # 返回过滤后的任务列表
    except:
        print("没有是这个项目经理的任务哦")

    try:
        if data['isfrozen']:
            tmp_tasks = tmp_tasks.filter_by(status=data['isfrozen'])
    except:
        print("没有状态为冻结的任务哦")

    # print(tmp_tasks.all())
    # print(tmp_projects.all())
    return tmp_tasks.all(), 201


@jwt_required()
def update_a_task(id):
    # 任务状态：Running|Freeze|Pause|Finish|Stop
    tmp_task = Task.query.filter_by(id=id).first()
    if not tmp_task:
        return response_with(ITEM_NOT_EXISTS)
    if tmp_task.islocked == True:
        return response_with(ITEM_LOCKED_400)
    update_val = request.json
    update_val['modifiedbyuid'] = get_jwt_identity()
    update_val['modifytime'] = datetime.now()
    wj2o(tmp_task, update_val)
    # update_val['islocked'] = tmp_task.islocked
    # update_val['isfrozen'] = tmp_task.isfrozen
    # update_val['isstop'] = tmp_task.isstop
    save_changes(tmp_task)
    response_object = {
        'code': 'success',
        'message': f'Task {id} updated!'.format()
    }
    return response_object, 201

@jwt_required()
def operate_a_task(id, operator):
    tmp_task = Task.query.filter_by(id=id).first()
    if not tmp_task:
        return response_with(ITEM_NOT_EXISTS)
    if tmp_task.islocked:
        if operator != "unlock":
            print("任务已经上锁")
            return response_with(ITEM_LOCKED_400)
        else:
            tmp_task.islocked = False
    else:
        if operator == "lock":
            tmp_task.islocked = True
        elif operator == "delete":
            db.session.delete(tmp_task)
        elif operator == "freeze":
            tmp_task.isfrozen = True
            tmp_task.status = 'freeze'
            tmp_task.freezetime = datetime.now()
            tmp_task.frozenbyuid = get_jwt_identity()
        elif operator == "unfreeze":
            tmp_task.isfrozen = False
            tmp_task.status = 'running'
            tmp_task.freezetime = None
            tmp_task.frozenbyuid = None
        elif operator == "pause":
            tmp_task.ispaused = True
            tmp_task.status = 'pause'
            tmp_task.pausetime = datetime.now()
            tmp_task.pausebyuid = get_jwt_identity()
        elif operator == "restart":
            if tmp_task.ispaused == True:
                tmp_task.ispaused = False
                tmp_task.status = 'running'
                tmp_task.pausetime = None
                tmp_task.pausebyuid = None
            else:
                return {
                        "http_status": 400,
                        "status": "itemNotPaused",
                        "message": "you can't restart a task while it's not paused."
                    }
        elif operator == "begin":
            if tmp_task.status != 'pause':
                # 如果任务暂停则说明已经开始
                tmp_task.status = 'running'
            else:
                return {
                        "http_status": 400,
                        "status": "itemNotNewBuilt",
                        "message": "you can only begin a newly built task."
                    }
        else:
            print("欸!?人家没有这种性能哦!")
            print("主人这是菜单（＞人＜；）-> (un)lock|delete|(un)freeze|(un)pause|begin")
            return "INVALID_INPUT", 422
    db.session.commit()
    response_object = {
        'code': 'success',
        'message': f'task {id} safely updated!'.format()
    }
    return response_object, 201


def save_changes(data: Task) -> None:
    db.session.add(data)
    db.session.commit()

# def send_mails_of_task(id):
#     mail = Mail()
#     tem_task = Task.query.filter_by(id=id).first()
#     target_id_list = json.loads(tem_task.target_id_list)
#     for uid in target_id_list:
#         tem_user = User.query.filter_by(id=uid).first()
#         reci = tem_user.email
#         msg = Message("qqHello "+str(uid), recipients=[reci])
#         msg.body = "Hello Flask message sent from Flask-Mail"
#         mail.send(msg)
#
#     response_object = {
#         'code': 'success',
#         'message': 'success'
#     }
#     return response_object, 201

