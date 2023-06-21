from flask import request
from app.main import db
from app.main.model.user import User
from app.main.model.project import Project
from app.main.model.organization import Organization
from typing import Dict, Tuple
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.main.util.write_json_to_obj import wj2o
from datetime import datetime
from app.main.service.log_service import save_log


def save_new_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    # 指定身份：sysrole | client | staff(被测)
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        new_user = User()
        data = request.json
        wj2o(new_user, data)
        if str(data['sysrole']) != 'sysrole' and str(data['sysrole']) != 'client' and str(data['sysrole']) != 'staff':
            print(data['sysrole'])
            return {
                       'status': 'fail',
                       'message': 'no such role. please choose between:sysrole/client/staff'
                   }, 404
        else:
            if str(data['sysrole']) == 'sysrole':
                # wj2o(new_user, data)
                new_user.orgid = 0
                save_changes(new_user)
                details = " create a new user."
                save_log("Create", get_jwt_identity(), details)
                return generate_token(new_user)
            else:
                print(new_user.orgid)
                if new_user.orgid == 0:
                    print(type(new_user.orgid))
                    return {
                               'status': 'fail',
                               'message': 'no such org ,org_id should >= 1'
                           }, 400
                else:
                    # wj2o(new_user, data)
                    save_changes(new_user)
                    details = " create a new user."
                    save_log("Create", get_jwt_identity(), details)
                    return generate_token(new_user)

    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409


def get_all_users():
    return User.query.all(), 200


def get_a_user(id):
    return User.query.filter_by(id=id).first()


def get_project_all_users(id):
    if Project.query.filter_by(id=id).first():
        print('?')
        org_id = Project.query.filter_by(id=id).first().orgid
        print('orgid', org_id)
        if org_id:
            users = User.query.filter_by(orgid=org_id, sysrole='staff').all()
            if users:
                return users, 200
            else:
                return {
                           'status': 'fail',
                           'message': 'no such user, please check the sysrole'
                       }, 404
        else:
            return {
                       'message': 'no such orgid',
                       'status': 'fail'
                   }, 404
    else:
        return {
                   'message': 'no such project id',
                   'status': 'fail'
               }, 404


def get_org_all_users(name):
    tmp_org = Organization.query.filter_by(name=name).first()
    if tmp_org:
        org_id = tmp_org.id
        print("here")
        if org_id != 0:
            users = User.query.filter_by(orgid=org_id, sysrole='client').all()
            if users:
                return users, 200
            else:
                return {
                           'status': 'fail',
                           'message': 'no such user, please check the sysrole'
                       }, 404
        else:
            return {
                       'message': 'no such client org',
                       'status': 'fail'
                   }, 404
    else:
        return {
                   'message': 'no such org',
                   'status': 'fail'
               }, 404


def generate_token(user: User) -> Tuple[Dict[str, str], int]:
    try:
        # generate the auth token
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': create_access_token(user.id)
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.' + str(e)
        }
        return response_object, 401


def get_users_by_org_id(id):
    users = User.query.filter_by(orgid=id).all()
    return users, 200

# @jwt_required()
def operate_a_user(id, operator):
    tmp_user = User.query.filter_by(id=id).first()
    operat_id = get_jwt_identity()
    operat_user = list(db.session.query(User.sysrole).filter(User.id == operat_id).first())[0]
    if operat_user == "staff":
        return f"no permission!", 403
    if not tmp_user:
        return "ITEM_NOT_EXISTS", 404
    if tmp_user.is_locked:
        if operator != "unlock":
            return "ITEM_LOCKED", 401
        else:
            tmp_user.is_locked = False
    else:
        if operator == "lock":
            tmp_user.is_locked = True
        elif operator == "delete":
            db.session.delete(tmp_user)
        elif operator == "freeze":
            tmp_user.is_frozen = True
            tmp_user.frozen_time = datetime.now()
            tmp_user.frozen_by = get_jwt_identity()
        elif operator == "unfreeze":
            tmp_user.is_frozen = False
            tmp_user.frozen_time = None
            tmp_user.frozen_by = None
        else:
            print("什么东西")
            return "INVALID_INPUT", 422
    db.session.commit()
    response_object = {
        'code': 'success',
        'message': f'User {id} {operator}!'.format().format()
    }
    details = " " + operator + " user " + str(id)
    save_log("Modify", get_jwt_identity(), details)
    return response_object, 201

# @jwt_required()
def delete_users():
    user = User.query.all()
    for tmp_user in user:
        db.session.delete(tmp_user)
    db.session.commit()
    details = " delete all users."
    save_new_user("Delete", get_jwt_identity(), details)
    return f"delete success", 201


def search_for_user(data):
    tmp_user = User.query
    try:
        if data['id']:
            print(data['id'])
            tmp_user = tmp_user.filter_by(id=data['id'])
    except:
        print("无id")

    try:
        if data['username']:
            tmp_user = tmp_user.filter(User.username.like("%" + data['username'] + "%"))
    except:
        print("无name")

    try:
        if data['sysrole']:
            tmp_user = tmp_user.filter(User.sysrole.like("%" + data['sysrole'] + "%"))
    except:
        print("无sysrole")

    try:
        if data['is_frozen']:
            tmp_user = tmp_user.filter_by(is_frozen=data['is_frozen'])
    except:
        print("无status")

    try:
        if data['orgid']:
            tmp_user = tmp_user.filter_by(orgid=data['orgid'])
    except:
        print("无orgid")

    print(tmp_user.all())
    return tmp_user.all(), 200


def save_changes(data: User) -> None:
    db.session.add(data)
    db.session.commit()


def update_a_user(id):
    tmp_user = User.query.filter_by(id=id).first()
    if not tmp_user:
        return "no that user", 404
    if tmp_user.is_locked == True:
        return "user record locked!", 401
    update_val = request.json
    # update_val['lastmodifiedbyuid'] = get_jwt_identity()
    wj2o(tmp_user, update_val)
    tmp_user.modified_time = datetime.now()
    save_changes(tmp_user)
    response_object = {
        'code': 'success',
        'message': f'User {id} updated!'.format()
    }
    details = " update user" + id
    save_log("Modify", get_jwt_identity(), details)
    return response_object, 201


def get_user_number():
    response_object = {
        'code': 'success',
        'number': User.query.count()
    }
    return response_object, 200
