from flask import request
from app.main import db
from app.main.model.project import Project
from app.main.model.user import User
from app.main.model.organization import Organization
from app.main.model.liaison import Liaison
from typing import Dict, Tuple
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.main.util.write_json_to_obj import wj2o
from datetime import datetime
from sqlalchemy import case, literal
from app.main.service.log_service import save_log

creator = db.aliased(User)
manager = db.aliased(User)


def get_all_projects():
    tmp_project = db.session.query(Project.id, Project.project_name,
                                   Project.project_creator_id, creator.username.label('project_creator_name'),
                                   creator.email.label('project_creator_email'),
                                   Project.client_id.label('project_manager_id'),
                                   manager.username.label('project_manager_name'),
                                   manager.email.label('project_manager_email'),
                                   Project.orgid.label('organization_id'), Organization.name.label('organization_name'),
                                   Project.status, Project.comment,
                                   Project.is_frozen,
                                   case([(Project.frozen_by.isnot(None), Project.frozen_by)], else_=literal("")).label(
                                       'frozen_by'),
                                   Project.is_locked,
                                   case([(Project.locked_by.isnot(None), Project.locked_by)], else_=literal("")).label(
                                       'locked_by'),
                                   Project.modified_time, Project.create_time, Project.end_time). \
        outerjoin(creator, Project.project_creator_id == creator.id). \
        outerjoin(manager, Project.client_id == manager.id). \
        outerjoin(Organization, Project.orgid == Organization.id).all()
    print(tmp_project)
    return tmp_project, 200


def get_all_project_ids():
    projects = Project.query.all()
    project_ids = [project.id for project in projects]
    return project_ids, 201


def save_new_project(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    project_exist = Project.query.filter_by(project_name=data['project_name']).first()
    manager_exist = User.query.filter(User.username == data['project_manager']).filter(User.sysrole == "client").first()
    org_exist = Organization.query.filter(Organization.name == data['organization_name']).first()
    creator_id = get_jwt_identity()
    creator_role = list(db.session.query(User.sysrole).filter_by(id=creator_id).first())[0]
    response_object = {
        'status': 'fail',
        'message': 'project already exists!',
    }
    if creator_role == "sysrole":
        if not project_exist:
            if manager_exist:
                if org_exist:
                    new_project = Project()
                    data = request.json
                    wj2o(new_project, data)
                    new_project.client_id = list(db.session.query(User.id).filter(User.username == data['project_manager']).first())[0]
                    new_project.project_creator_id = get_jwt_identity()
                    new_project.orgid = list(db.session.query(Organization.id).filter(Organization.name == data['organization_name']).first())[0]
                    save_changes(new_project)
                    response_object['status'] = 'success'
                    response_object['message'] = 'project created!'
                    save_log("Create", get_jwt_identity(), " create a project.")
                    return response_object, 201
                    # return generate_token(new_project)
                else:
                    response_object['message'] = 'no such organization!'
                    return response_object, 404
            else:
                response_object['message'] = 'no such client manager!'
                return response_object, 404
        else:
            return response_object, 409
    else:
        response_object['message'] = 'you are not the sysrole!'
        return response_object, 403


def delete_projects():
    operator_id = get_jwt_identity()
    operator_role = list(db.session.query(User.sysrole).filter_by(id=operator_id).first())[0]
    if operator_role == "sysrole" or operator_role == "client":
        project = Project.query.all()
        for tmp_project in project:
            db.session.delete(tmp_project)
        db.session.commit()
        save_log("Delete", get_jwt_identity(), " delete all projects!")
        return f"delete success", 201
    else:
        return f"no permission", 403


def get_a_project(id):
    tmp_project = db.session.query(Project.id, Project.project_name,
                                   Project.project_creator_id, creator.username.label('project_creator_name'),
                                   creator.email.label('project_creator_email'),
                                   Project.client_id.label('project_manager_id'),
                                   manager.username.label('project_manager_name'),
                                   manager.email.label('project_manager_email'),
                                   Project.orgid.label('organization_id'), Organization.name.label('organization_name'),
                                   Project.status, Project.comment,
                                   Project.is_frozen,
                                   case([(Project.frozen_by.isnot(None), Project.frozen_by)], else_=literal("")).label(
                                       'frozen_by'),
                                   Project.is_locked,
                                   case([(Project.locked_by.isnot(None), Project.locked_by)], else_=literal("")).label(
                                       'locked_by'),
                                   Project.modified_time, Project.create_time, Project.end_time). \
        outerjoin(creator, Project.project_creator_id == creator.id). \
        outerjoin(manager, Project.client_id == manager.id). \
        outerjoin(Organization, Project.orgid == Organization.id).\
        filter(Project.id == id).first()
    return tmp_project


def operate_a_project(id, operator):
    operator_id = get_jwt_identity()
    operator_role = list(db.session.query(User.sysrole).filter_by(id=operator_id).first())[0]
    tmp_project = Project.query.filter_by(id=id).first()
    if operator_role == "sysrole" or operator_role == "client":
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
                tmp_project.status = "Froze"
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
            elif operator == "Froze":
                tmp_project.status = "Froze"
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
        details = " " + operator + " project " + id
        save_log("Modify", get_jwt_identity(), details)
        return response_object, 201
    else:
        return f"no permission", 403


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
