from app.main.model.mail_template import Mailtemplate
from datetime import datetime
from flask import request
from app.main import db
from typing import Dict, Tuple
from flask_jwt_extended import get_jwt_identity, jwt_required
from config import QMailConfig


from app.main.model.task import Task
from app.main.model.user import User
from app.main.util.response_tip import *
from app.main.util.write_json_to_obj import wj2o

def get_all_mail_templates():
    return Mailtemplate.query.all(), 201

def get_a_mail_template(id):
    return Mailtemplate.query.filter_by(id=id).first(), 201

def get_all_mail_ids():
    mails = Mailtemplate.query.all()
    mail_ids = [mail.id for mail in mails]
    return mail_ids, 201

@jwt_required()
def save_new_mail_template(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    template = Mailtemplate.query.filter_by(subject=data['subject']).first()
    if not template:
        new_template = Mailtemplate()
        data = request.json
        data['createdbyuid'] = get_jwt_identity()
        wj2o(new_template, data)
        save_changes(new_template)
        return response_with(SUCCESS_201)
    else:
        response_object = {
            'status': 'fail',
            'message': 'MailTemplate already exists.',
        }
        return response_object, 409

def search_for_mail_templates(data):
    # print("here")
    tmp_templates = Mailtemplate.query
    try:
        if data['id']:
            print(data['id'])
            tmp_templates = tmp_templates.filter_by(id=data['id'])
    except:
        print("无id")

    try:
        if data['partial_name']:
            tmp_templates = tmp_templates.filter(Mailtemplate.subject.like("%" + data['partial_name'] + "%"))
    except:
        print("无subject")

    try:
        if data['create_time_start'] and data['create_time_end']:
            tmp_templates = tmp_templates.filter(Mailtemplate.createtime.between(data['create_time_start'], data['create_time_end']))
            print(tmp_templates.all())
    except Exception as e:
        print("无create", e)

    try:
        if data['modify_time_start'] and data['modify_time_end']:
            tmp_templates = tmp_templates.filter(Mailtemplate.modifytime.between(data['modify_time_start'], data['modify_time_end']))
    except:
        print("无modi")

    try:
        if data['islocked']:
            tmp_templates = tmp_templates.filter_by(status=data['islocked'])
    except:
        print("无locked")




    print(tmp_templates.all())
    return tmp_templates.all(), 201

def operate_a_mail_template(id, operator):
    """
    操作包含：锁定|解锁、删除
    Args:
        id: organization id
        operator:

    Returns:

    """
    tmp_template = Mailtemplate.query.filter_by(id=id).first()

    if not tmp_template:
        return response_with(ITEM_NOT_EXISTS)
    if tmp_template.islocked:
        if operator != "unlock":
            print('锁了')
            return response_with(ITEM_LOCKED_400)
        else:
            tmp_template.islocked = False
    else:
        if operator == "lock":
            tmp_template.islocked = True
        elif operator == "delete":
            db.session.delete(tmp_template)

        else:
            print("日怪嘞")
            return response_with(INVALID_INPUT_422)

    db.session.commit()
    return response_with(SUCCESS_201)

@jwt_required()
def update_a_mail_template(id):
    tmp_template = Mailtemplate.query.filter_by(id=id).first()
    if not tmp_template:
        return response_with(ITEM_NOT_EXISTS)
    if tmp_template.islocked == True:
        return response_with(ITEM_LOCKED_400)
    update_val = request.json
    update_val['modifiedbyuid'] = get_jwt_identity()
    update_val['modifytime'] = datetime.now()
    update_val['islocked'] = tmp_template.islocked
    update_val['isfrozen'] = tmp_template.isfrozen
    wj2o(tmp_template, update_val)
    save_changes(tmp_template)
    response_object = {
        'code': 'success',
        'message': f'Template {id} updated!'.format()
    }
    return response_object, 201




def save_changes(data: Mailtemplate) -> None:
    db.session.add(data)
    db.session.commit()








