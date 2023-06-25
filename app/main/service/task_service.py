from flask import request, render_template_string
from app.main import db, scheduler
from app.main.model.task import Task
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
import ast
from app.main.service.log_service import save_log

running_jobs = {}


@jwt_required()
def save_new_task(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    task = Task.query.filter_by(name=data['name']).first()
    project_exist = Project.query.filter(Project.id == data['project_id']).first()
    mail_exist = Mailtemplate.query.filter(Mailtemplate.id == data['mail_id']).first()
    catcher_exist = Servercatcher.query.filter(Servercatcher.id == data['catcher_id']).first()
    mail_server_exist = Serversender.query.filter(Serversender.id == data['mail_server_id']).first()
    if not task:
        if project_exist:
            if mail_exist:
                if catcher_exist:
                    if mail_server_exist:
                        new_task = Task()
                        data = request.json
                        data['createdbyuid'] = get_jwt_identity()
                        wj2o(new_task, data)
                        if new_task.type == 'mail':
                            date_format = '%Y-%m-%d %H:%M:%S.%f'
                            date_time = datetime.strptime(new_task.delivery_time, date_format)
                            new_task.delivery_time = date_time
                            new_task.target_num = len(eval(str(new_task.target_id_list)))

                            if date_time < datetime.now():
                                return {
                                           "code": "timeisnotallowed",
                                           "message": "time is earlier than now!!"
                                       }, 405
                            else:
                                save_changes(new_task)
                                job_id = "task_" + str(new_task.id)
                                ulist = get_a_task_users(new_task.id)
                                print(ulist)

                                running_jobs[job_id] = {'tid': new_task.id, 'u_list': ulist, 'interval_seconds': new_task.delivery_freq,
                                                        'sendlist': [], 'retry': 0, 'sender': new_task.mail_server_id, 'catcher': new_task.catcher_id}


                                scheduler.add_job(func=send_mails, trigger='interval', args=[job_id], id=job_id,
                                                  seconds=new_task.delivery_freq, start_date=new_task.delivery_time)
                                details = " create a new task."
                                save_log("Create", get_jwt_identity(), details)
                                return response_with(SUCCESS_201)
                        elif new_task.type == 'qrcode':
                            new_task.delivery_time = datetime.now()
                            new_task.target_num = len(eval(str(new_task.target_id_list)))
                            save_changes(new_task)
                            details = " create a new task."
                            save_log("Create", get_jwt_identity(), details)
                            return response_with(SUCCESS_201)
                        else:
                            return {
                                       "code": "typeNotSupport",
                                       "message": "only mail and qrcode is support."
                                   }, 405
                    else:
                        return {
                                   "code": "serverNotExist",
                                   "message": "no such mail server, sorry you can't add."
                               }, 404
                else:
                    return {
                               "code": "catcherNotExist",
                               "message": "no such catcher server, sorry you can't add."
                           }, 404
            else:
                return {
                           "code": "mailNotExist",
                           "message": "no such mail, sorry you can't add."
                       }, 404
        else:
            return {
                       "code": "projectNotExist",
                       "message": "no such project, sorry you can't add."
                   }, 404
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


def get_a_task_users(tid):
    tem_task = Task.query.filter_by(id=tid).first()
    u_list = json.loads(tem_task.target_id_list)
    return u_list


def search_for_tasks(data):
    # 编号、名称、创建日期、修改日期、项目id、项目名称、项目经理id、冻结状态
    tmp_tasks = Task.query
    tmp_projects = Project.query

    try:
        if data['id']:
            print(data['id'])
            tmp_tasks = tmp_tasks.filter_by(id=data['id'])
            return tmp_tasks.all(), 201
    except:
        print("没有是这个编号的任务哦")

    try:
        if data['name']:
            tmp_tasks = tmp_tasks.filter(Task.name.like("%" + data['name'] + "%"))
            return tmp_tasks.all(), 201
    except:
        print("没有是这个名称的任务哦")

    try:
        if data['create_time_begin'] and data['create_time_end']:
            tmp_tasks = tmp_tasks.filter(
                Task.createtime.between(data['create_time_start'], data['create_time_end']))
            # print(tmp_tasks.all())
            return tmp_tasks.all(), 201
    except Exception as e:
        print("没有在这个时间区间内创建的任务哦", e)

    try:
        if data['modify_time_start'] and data['modify_time_end']:
            tmp_tasks = tmp_tasks.filter(
                Task.modifytime.between(data['modify_time_start'], data['modify_time_end']))
            return tmp_tasks.all(), 201
    except:
        print("没有在这个时间区间修改的任务哦")

    try:
        if data['project_id']:
            tmp_tasks = tmp_tasks.filter_by(project_id=data['project_id'])
            return tmp_tasks.all(), 201
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
            return tmp_tasks.all(), 201
    except:
        print("没有状态为冻结的任务哦")

    # print(tmp_tasks.all())
    # print(tmp_projects.all())
    return {
               'status': 'fail',
               'message': '看上去没有搜索任何东西呢'
           }, 404


@jwt_required()
def update_a_task(id):
    # update task info ,status not included
    tmp_task = Task.query.filter_by(id=id).first()
    old_delivery_time = tmp_task.delivery_time
    old_target_id_list = tmp_task.target_id_list
    old_frq = tmp_task.delivery_freq
    if not tmp_task:
        return response_with(ITEM_NOT_EXISTS)
    if tmp_task.islocked:
        return response_with(ITEM_LOCKED_400)
    if tmp_task.status == 'finish':
        return {
                   "code": "taskHasFinished",
                   "message": "cannot modify a finish task."
               }, 405
    elif tmp_task.status == 'running':
        return {
                   "code": "taskRunning",
                   "message": "cannot modify a running task."
               }, 405
    elif tmp_task.status == 'waiting':
        update_val = request.json
        update_val['modifiedbyuid'] = get_jwt_identity()
        update_val['modifytime'] = datetime.now()
        wj2o(tmp_task, update_val)
        date_format = '%Y-%m-%d %H:%M:%S.%f'
        date_time = datetime.strptime(tmp_task.delivery_time, date_format)
        tmp_task.delivery_time = date_time
        if date_time < datetime.now():
            return {
                       "code": "timeisnotallowed",
                       "message": "time is earlier than now!!"
                   }, 405
        else:
            save_changes(tmp_task)
            job_id = "task_" + str(tmp_task.id)
            ulist = get_a_task_users(tmp_task.id)
            print(ulist)
            try:
                scheduler.remove_job(job_id)
            except Exception as e:
                print(e)
            running_jobs[job_id] = {'tid': tmp_task.id, 'u_list': ulist, 'interval_seconds': tmp_task.delivery_freq,
                                    'sendlist': [], 'retry': 0, 'sender': tmp_task.mail_server_id, 'catcher': tmp_task.catcher_id}

            scheduler.add_job(func=send_mails, trigger='interval', args=[job_id], id=job_id,
                              seconds=tmp_task.delivery_freq, start_date=tmp_task.delivery_time)
            response_object = {
                'code': 'success',
                'message': f'Task {id} updated!'.format()
            }
            return response_object, 201
    elif tmp_task.status == 'frozen':
        update_val = request.json
        update_val['modifiedbyuid'] = get_jwt_identity()
        update_val['modifytime'] = datetime.now()
        wj2o(tmp_task, update_val)
        date_format = '%Y-%m-%d %H:%M:%S.%f'
        date_time = datetime.strptime(tmp_task.delivery_time, date_format)
        tmp_task.delivery_time = date_time
        # if delivery_freq is not changed
        if tmp_task.delivery_time == old_delivery_time and tmp_task.target_id_list == old_target_id_list and tmp_task.delivery_freq == old_frq:
            job_id = "task_" + str(tmp_task.id)
            running_jobs[job_id]['sender'] = tmp_task.mail_server_id
            running_jobs[job_id]['catcher'] = tmp_task.catcher_id
            save_changes(tmp_task)
            response_object = {
                'code': 'success',
                'message': f'Task {id} updated!'.format()
            }
            return response_object, 201
        # if delivery_freq is changed
        elif tmp_task.delivery_time == old_delivery_time and tmp_task.target_id_list == old_target_id_list:
            save_changes(tmp_task)
            job_id = "task_" + str(tmp_task.id)
            scheduler.remove_job(job_id)
            running_jobs[job_id]['sender'] = tmp_task.mail_server_id
            running_jobs[job_id]['catcher'] = tmp_task.catcher_id
            running_jobs[job_id]['interval_seconds'] = tmp_task.delivery_freq
            scheduler.add_job(func=send_mails, trigger='interval', args=[job_id], id=job_id,
                              seconds=tmp_task.delivery_freq, start_date=tmp_task.delivery_time)
            scheduler.pause_job(id=job_id)
            response_object = {
                'code': 'success',
                'message': f'Task {id} updated!'.format()
            }
            return response_object, 201

        else:
            if date_time < datetime.now():
                return {
                           "code": "timeisnotallowed",
                           "message": "time is earlier than now!!"
                       }, 405
            else:
                save_changes(tmp_task)
                job_id = "task_" + str(tmp_task.id)
                ulist = get_a_task_users(tmp_task.id)
                print(ulist)
                scheduler.remove_job(job_id)
                running_jobs[job_id] = {'tid': tmp_task.id, 'u_list': ulist, 'interval_seconds': tmp_task.delivery_freq,
                                        'sendlist': [], 'retry': 0, 'sender': tmp_task.mail_server_id, 'catcher': tmp_task.catcher_id}
                scheduler.add_job(func=send_mails, trigger='interval', args=[job_id], id=job_id,
                                  seconds=tmp_task.delivery_freq, start_date=tmp_task.delivery_time)
                scheduler.pause_job(id=job_id)
                response_object = {
                    'code': 'success',
                    'message': f'Task {id} updated!'.format()
                }
                details = " update task " + str(id)
                return response_object, 201


@jwt_required()
def operate_a_task(tid, operator):
    tmp_task = Task.query.filter_by(id=tid).first()
    if not tmp_task:
        return response_with(ITEM_NOT_EXISTS)

    if tmp_task.islocked:
        if operator != "unlock":
            print("任务已经上锁")
            return response_with(ITEM_LOCKED_400)
        else:
            tmp_task.islocked = False
            tmp_task.locktime = None
            tmp_task.lockbyuid = None
    else:
        if operator == "lock":
            tmp_task.islocked = True
            tmp_task.locktime = datetime.now()
            tmp_task.lockbyuid = get_jwt_identity()
        elif operator == "delete":
            db.session.delete(tmp_task)
            if tmp_task.type == 'mail':
                job_id = "task_" + str(tid)
                try:
                    scheduler.remove_job(job_id)
                    if job_id in running_jobs:
                        del running_jobs[job_id]
                except Exception as e:
                    print(e)
        elif tmp_task.type == 'qrcode':
            return {
                       "code": "qrcodeTaskNotAllowed",
                       "message": "qrcode task is not allowed this operation."
                   }, 400
        elif tmp_task.status == 'finish':
            return {
                       "code": "itemisFinished",
                       "message": "the task is finished, please create a new one."
                   }, 400
        else:
            if operator == "freeze":
                if tmp_task.status == 'running':
                    tmp_task.ispaused = True
                    tmp_task.status = 'frozen'
                    tmp_task.freezetime = datetime.now()
                    tmp_task.frozenbyuid = get_jwt_identity()
                    job_id = "task_" + str(tid)
                    if job_id in running_jobs:
                        scheduler.pause_job(id=job_id)
                    else:
                        print('task is not running!!!')
                else:
                    print('task is not running!!!')
            elif operator == "unfreeze":
                if tmp_task.status == 'frozen':
                    tmp_task.ispaused = False
                    tmp_task.status = 'running'
                    tmp_task.pausetime = None
                    tmp_task.pausebyuid = None
                    job_id = "task_" + str(tid)
                    if job_id in running_jobs:
                        scheduler.resume_job(id=job_id)
                    else:
                        print('task is not running!!!')
                else:
                    return {
                               "code": "itemNotFrozen",
                               "message": "you can't unfreeze a task if it is not frozen."
                           }, 400
            # elif operator == "begin":
            #     if tmp_task.status == 'waiting':
            #         tmp_task.status = 'running'
            #         tmp_task.delivery_time = datetime.now()
            #         ulist = get_a_task_users(tid)
            #
            #         job_id = "task_"+str(tid)
            #         running_jobs[job_id] = {'tid': tid, 'u_list': ulist, 'interval_seconds': tmp_task.delivery_freq, 'sendlist': []}
            #         print(ulist)
            #         scheduler.add_job(func=send_mails, trigger='interval', args=[job_id], id=job_id, seconds=tmp_task.delivery_freq)
            #     else:
            #         print()
            #         return {
            #             "code": "itemNotWaiting",
            #             "message": "you can't begin a task if it is not waiting."
            #         }, 400

            else:
                print("欸!?人家没有这种性能哦!")
                print("主人这是菜单（＞人＜；）-> (un)lock|delete|(un)freeze|begin")
                return "INVALID_INPUT", 422
    db.session.commit()
    response_object = {
        'code': 'success',
        'message': f'task {tid} safely updated!'.format()
    }
    details = " " + operator + " task " + str(id)
    save_log("Modify", get_jwt_identity(), details)
    return response_object, 201


def send_mails(job_id):
    with app.app_context():
        if job_id in running_jobs:
            ulist = running_jobs[job_id]['u_list']
            sendlist = running_jobs[job_id]['sendlist']


            tmp_task = Task.query.filter_by(id=running_jobs[job_id]['tid']).first()
            tmp_sender = Serversender.query.filter_by(id=running_jobs[job_id]['sender']).first()
            tmp_catcher = Servercatcher.query.filter_by(id=running_jobs[job_id]['catcher']).first()

            if len(sendlist) < len(ulist):
                tmp_task.status = 'running'
                tmp_sender.status = 'busy'
                mailtempid = tmp_task.mail_id
                tmp_mtemplate = Mailtemplate.query.filter_by(id=mailtempid).first()
                subject = tmp_mtemplate.subject
                content = tmp_mtemplate.content
                next_uid = [u for u in ulist if u not in sendlist][0]
                tmp_user = User.query.filter_by(id=next_uid).first()
                tmp_em = tmp_user.email
                tmp_name = tmp_user.username
                tmp_url = 'http://' + tmp_catcher.server + ':' + str(tmp_catcher.port)
                db.session.commit()
                user = {'name': tmp_name, 'uid': next_uid, 'tid': running_jobs[job_id]['tid'], 'url': tmp_url}
                content = render_template_string(content, user=user)
                print(content)
                try:
                    send_mail(tmp_em, tmp_name, subject, content, tmp_sender)
                except Exception as e:
                    running_jobs[job_id]['retry'] += 1
                    print(running_jobs[job_id]['retry'])
                    if running_jobs[job_id]['retry'] >= 3:
                        print('重试失败')
                        running_jobs[job_id]['sendlist'].append(next_uid)
                        running_jobs[job_id]['retry'] = 0
                else:
                    running_jobs[job_id]['sendlist'].append(next_uid)
                    running_jobs[job_id]['retry'] = 0
            else:
                tmp_task.status = 'finish'
                tmp_sender.status = 'open'
                try:
                    scheduler.remove_job(job_id)
                    del running_jobs[job_id]
                except Exception as e:
                    print(e)
                db.session.commit()

        else:
            # scheduler.remove_job(job_id)
            print('任务未在进行，可能已结束或未开始')


def save_changes(data: Task) -> None:
    db.session.add(data)
    db.session.commit()


def send_mail(to_addr, name, subject, context, sender):
    mail = Mail()
    app.config.from_mapping(
        MAIL_SERVER=sender.server,
        MAIL_PORT=sender.port,
        MAIL_USERNAME=sender.name,
        MAIL_PASSWORD=sender.password
    )
    mail.init_app(app)
    with app.app_context():
        msg = Message(name + subject, recipients=[to_addr])
        msg.html = context
        mail.send(msg)


def get_task_number():
    response_object = {
        'code': 'success',
        'number': Task.query.count()
    }
    return response_object, 200
