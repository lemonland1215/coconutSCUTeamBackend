from flask import request
from app.main import db
from app.main.model.project import Project
from app.main.model.user import User
from app.main.model.liaison import Liaison
from app.main.model.organization import Organization
from typing import Dict, Tuple
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.main.util.write_json_to_obj import wj2o
from datetime import datetime


def get_all_projects():
    tmp_project = db.session.query(Project.id, Project.projectname, User.username.label('project_manager'),
                                   Project.customer_contact, Project.contact_email,
                                   Liaison.liaison_name.label('liaison_name'),
                                   Liaison.liaison_email.label('liaison_email'), Project.test_number,
                                   Project.is_frozen, Project.is_locked, Project.comment, Project.status,
                                   Organization.name.label('organization_name'), Project.create_time,
                                   Project.modified_time, Project.orgid, Project.liaison_id). \
        outerjoin(User, Project.project_manager_id == User.id). \
        outerjoin(Liaison, Project.liaison_id == Liaison.liaison_id). \
        outerjoin(Organization, Project.orgid == Organization.id)
    print(tmp_project.all())
    return tmp_project.all()


def get_all_project_ids():
    projects = Project.query.all()
    project_ids = [project.id for project in projects]
    return project_ids, 201

def save_new_project(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    project = Project.query.filter_by(projectname=data['projectname']).first()
    manager_exist = User.query.filter(User.id == data['project_manager_id']).first()
    liaison_exist = User.query.filter(User.id == data['liaison_id']).first()
    org_exist = Organization.query.filter(Organization.id == data['orgid']).first()
    response_object = {
        'status': 'fail',
        'message': 'project already exists!',
    }
    if not project:
        if manager_exist:
            if liaison_exist:
                if org_exist:
                    new_project = Project()
                    data = request.json
                    wj2o(new_project, data)
                    new_project.project_creator_id = get_jwt_identity()
                    new_project.orgname = \
                        list(db.session.query(Organization.name).filter(Organization.id == data['orgid']).first())[0]
                    print(data['liaison_id'])
                    liaison = db.session.query(Liaison).filter(Liaison.liaison_id == data['liaison_id']).first()
                    if not liaison:
                        new_liaison = Liaison()
                        new_liaison.liaison_id = data['liaison_id']
                        user = list(
                            db.session.query(User.username, User.email).filter(User.id == data['liaison_id']).first())
                        new_liaison.liaison_name = user[0]
                        new_liaison.liaison_email = user[1]
                        save_changes(new_liaison)
                    save_changes(new_project)
                    response_object['status'] = 'success'
                    response_object['message'] = 'project created!'
                    return response_object, 201
                    # return generate_token(new_project)
                else:
                    response_object['message'] = 'no such organization!'
                    return response_object, 404
            else:
                response_object['message'] = 'no such liaison!'
                return response_object, 404
        else:
            response_object['message'] = 'no such manager!'
            return response_object, 404
    else:
        return response_object, 409


def delete_projects():
    project = Project.query.all()
    liaison = Liaison.query.all()
    for tmp_project in project:
        db.session.delete(tmp_project)
    for tmp_liaison in liaison:
        db.session.delete(tmp_liaison)
    db.session.commit()
    return f"delete success", 201


def get_a_project(id):
    tmp_project = db.session.query(Project.id, Project.projectname, User.username.label('project_manager'),
                                   Project.customer_contact, Project.contact_email,
                                   Liaison.liaison_name.label('liaison_name'),
                                   Liaison.liaison_email.label('liaison_email'), Project.test_number,
                                   Project.is_frozen, Project.is_locked, Project.comment, Project.status,
                                   Organization.name.label('organization_name'),
                                   Project.create_time, Project.modified_time, Project.orgid, Project.liaison_id). \
        outerjoin(User, Project.project_manager_id == User.id). \
        outerjoin(Liaison, Project.liaison_id == Liaison.liaison_id). \
        outerjoin(Organization, Project.orgid == Organization.id). \
        filter(Project.id == id).first()
    print(tmp_project)
    return tmp_project


def operate_a_project(id, operator):
    tmp_project = Project.query.filter_by(id=id).first()
    if not tmp_project:
        return "ITEM_NOT_EXISTS", 404
    if tmp_project.is_locked:
        if operator == "lock":
            return "ITEM ALREADY LOCKED!", 200
        elif operator != "unlock":
            return "ITEM_LOCKED", 401
        else:
            tmp_project.is_locked = False
            tmp_project.locked_time = None
            tmp_project.locked_by = None
    else:
        if operator == "lock":
            tmp_project.is_locked = True
            tmp_project.locked_time = datetime.now()
            tmp_project.locked_by = get_jwt_identity()
        elif operator == "delete":
            db.session.delete(tmp_project)
        elif operator == "freeze":
            tmp_project.is_frozen = True
            tmp_project.status = "Pause"
            tmp_project.frozen_time = datetime.now()
            tmp_project.modified_time = datetime.now()
            tmp_project.frozen_by = get_jwt_identity()
        elif operator == "unfreeze":
            tmp_project.is_frozen = False
            tmp_project.status = "Running"
            tmp_project.frozen_time = None
            tmp_project.modified_time = datetime.now()
            tmp_project.frozen_by = None
        elif operator == "Running":
            tmp_project.status = "Running"
            tmp_project.modified_time = datetime.now()
        elif operator == "Pause":
            tmp_project.status = "Pause"
            tmp_project.modified_time = datetime.now()
        elif operator == "Finish":
            tmp_project.status = "Finish"
            tmp_project.modified_time = datetime.now()
        elif operator == "Stop":
            tmp_project.status = "Stop"
            tmp_project.modified_time = datetime.now()
        elif operator == "unlock":
            return "ALREADY UNLOCKED!", 200
        else:
            print("什么东西")
            return "INVALID_INPUT", 422
    db.session.commit()
    response_object = {
        'code': 'success',
        'message': f'project {id} {operator}!'.format().format()
    }
    return response_object, 201


def search_for_project(data):
    tmp_project = db.session.query(Project.id, Project.projectname, User.username.label('project_manager'),
                                   Project.customer_contact, Project.contact_email,
                                   Liaison.liaison_name.label('liaison_name'),
                                   Liaison.liaison_email.label('liaison_email'), Project.test_number,
                                   Project.is_frozen, Project.comment, Project.status,
                                   Organization.name.label('organization_name'), Project.create_time,
                                   Project.is_locked, Project.modified_time). \
        outerjoin(User, Project.project_manager_id == User.id). \
        outerjoin(Liaison, Project.liaison_id == Liaison.liaison_id). \
        outerjoin(Organization, Project.orgid == Organization.id)

    try:
        if data['id']:
            tmp_project = tmp_project.filter(Project.id == data['id'])
    except:
        print("no such id")

    try:
        if data['projectname']:
            tmp_project = tmp_project.filter(Project.projectname.like("%" + data['projectname'] + "%"))
    except:
        print("no such projectname")

    try:
        if data['orgid']:
            tmp_project = tmp_project.filter(Project.orgid == data['orgid'])
    except:
        print("no such orgid")

    try:
        if data['orgname']:
            tmp_project = tmp_project.filter(Organization.name.like("%" + data['orgname'] + "%"))
    except:
        print("no such orgname")

    try:
        if data['is_frozen']:
            tmp_project = tmp_project.filter(Project.is_frozen == data['is_frozen'])
    except:
        print("no frozen projects")

    try:
        if data['create_time']:
            tmp_project = tmp_project.filter(Project.create_time.like("%" + data['create_time'] + "%"))
    except:
        print(("no such create time"))

    try:
        if data['modified_time']:
            tmp_project = tmp_project.filter(Project.modified_time.like("%" + data['modified_time'] + "%"))
    except:
        print(("no such modified time"))

    try:
        if data['manager_name']:
            tmp_project = tmp_project.filter(User.username.like("%" + data['create_time'] + "%"))
    except:
        print(("no such manager"))

    print(tmp_project.all())
    return tmp_project.all(), 201


def save_changes(data: Project) -> None:
    db.session.add(data)
    db.session.commit()


@jwt_required()
def update_a_project(id):
    tmp_project = Project.query.filter_by(id=id).first()
    if not tmp_project:
        return "no that project", 404
    if tmp_project.is_locked == True:
        return "project locked!", 401
    update_val = request.json
    projectname_exist = Project.query.filter(Project.projectname == update_val['projectname']).first()
    if projectname_exist and projectname_exist.id != int(id):
        return "conflict name!", 409
    # 如果有经理id
    if User.query.filter(User.id == update_val['project_manager_id']).first():
        # 如果有联系人id
        if User.query.filter(User.id == update_val['liaison_id']).first():
            # 如果新的联系人不在表内，添加新的联系人，不用删除旧的联系人
            if not Liaison.query.filter(Liaison.liaison_id == update_val['liaison_id']).first():
                tmp_liaison = Liaison()
                tmp_liaison.liaison_id = update_val['liaison_id']
                user = list(
                    db.session.query(User.username, User.email).filter(User.id == update_val['liaison_id']).first())
                tmp_liaison.liaison_name = user[0]
                tmp_liaison.liaison_email = user[1]
                save_changes(tmp_liaison)
            # 如果新的联系人在表内，不做更改
            wj2o(tmp_project, update_val)
            print(update_val)
            tmp_project.modified_time = datetime.now()
            save_changes(tmp_project)
            response_object = {
                'code': 'success',
                'message': f'project {id} updated!'.format()
            }
            return response_object, 201
        # 如果没有联系人id
        else:
            return "no such liaison!", 404
    # 如果没有经理id
    else:
        return "no such manager!", 404


def get_projects_by_org_id(id):
    projects = Project.query.filter_by(orgid=id).all()
    return projects, 201
