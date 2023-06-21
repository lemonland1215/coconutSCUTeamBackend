from flask import request
from app.main import db
from app.main.model.project import Project
from app.main.model.user import User
from app.main.model.organization import Organization
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
                                   case((Project.frozen_by.isnot(None), Project.frozen_by), else_=literal("")).label(
                                       'frozen_by'),
                                   Project.is_locked,
                                   case((Project.locked_by.isnot(None), Project.locked_by), else_=literal("")).label(
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
        'code': 'fail',
        'message': 'project already exists!',
    }
    if creator_role == "sysrole":
        if not project_exist:
            if manager_exist:
                if org_exist:
                    new_project = Project()
                    data = request.json
                    wj2o(new_project, data)
                    new_project.client_id = \
                        list(db.session.query(User.id).filter(User.username == data['project_manager']).first())[0]
                    new_project.project_creator_id = get_jwt_identity()
                    new_project.orgid = list(db.session.query(Organization.id).filter(
                        Organization.name == data['organization_name']).first())[0]
                    save_changes(new_project)
                    response_object['code'] = 'success'
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
        return response_object, 401


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
        return f"no permission", 401


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
                                   case((Project.frozen_by.isnot(None), Project.frozen_by), else_=literal("")).label(
                                       'frozen_by'),
                                   Project.is_locked,
                                   case((Project.locked_by.isnot(None), Project.locked_by), else_=literal("")).label(
                                       'locked_by'),
                                   Project.modified_time, Project.create_time, Project.end_time). \
        outerjoin(creator, Project.project_creator_id == creator.id). \
        outerjoin(manager, Project.client_id == manager.id). \
        outerjoin(Organization, Project.orgid == Organization.id). \
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
                tmp_project.status = "Frozen"
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
            elif operator == "Frozen":
                tmp_project.status = "Frozen"
                tmp_project.modified_time = datetime.now()
            elif operator == "Finish":
                tmp_project.status = "Finish"
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
        details = " " + operator + " project " + str(id)
        save_log("Modify", get_jwt_identity(), details)
        return response_object, 201
    else:
        return f"no permission", 401


def search_for_project(data):
    tmp_project = db.session.query(Project.id, Project.project_name,
                                   Project.project_creator_id, creator.username.label('project_creator_name'),
                                   creator.email.label('project_creator_email'),
                                   Project.client_id.label('project_manager_id'),
                                   manager.username.label('project_manager_name'),
                                   manager.email.label('project_manager_email'),
                                   Project.orgid.label('organization_id'), Organization.name.label('organization_name'),
                                   Project.status, Project.comment,
                                   Project.is_frozen,
                                   case((Project.frozen_by.isnot(None), Project.frozen_by), else_=literal("")).label(
                                       'frozen_by'),
                                   Project.is_locked,
                                   case((Project.locked_by.isnot(None), Project.locked_by), else_=literal("")).label(
                                       'locked_by'),
                                   Project.modified_time, Project.create_time, Project.end_time). \
        outerjoin(creator, Project.project_creator_id == creator.id). \
        outerjoin(manager, Project.client_id == manager.id). \
        outerjoin(Organization, Project.orgid == Organization.id)

    try:
        if data['id']:
            tmp_project = tmp_project.filter(Project.id == data['id'])
    except:
        print("no such id")

    try:
        if data['project_name']:
            tmp_project = tmp_project.filter(Project.project_name.like("%" + data['project_name'] + "%"))
    except:
        print("no such project name")

    try:
        if data['project_creator_id']:
            tmp_project = tmp_project.filter(Project.project_creator_id == data['project_creator_id'])
    except:
        print("no such creator id")

    try:
        if data['project_creator_name']:
            tmp_project = tmp_project.filter(creator.username.like("%" + data['project_creator_name'] + "%")). \
                filter(creator.sysrole == "sysrole")
    except:
        print("no such creator name")

    try:
        if data['project_manager_id']:
            tmp_project = tmp_project.filter(Project.client_id == data['project_manager_id'])
    except:
        print("no such manager id")

    try:
        if data['project_manager_name']:
            tmp_project = tmp_project.filter(manager.username.like("%" + data['project_client_name'] + "%")). \
                filter(manager.sysrole == "client")
    except:
        print("no such client name")

    try:
        if data['organization_id']:
            tmp_project = tmp_project.filter(Project.orgid == data['organization_id'])
    except:
        print("no such orgid")

    try:
        if data['organization_name']:
            tmp_project = tmp_project.filter(Organization.name.like("%" + data['organization_name'] + "%"))
    except:
        print("no such orgname")

    try:
        if data['is_frozen']:
            tmp_project = tmp_project.filter(Project.is_frozen == data['is_frozen'])
    except:
        print("no frozen projects")

    try:
        if data['is_locked']:
            tmp_project = tmp_project.filter(Project.is_locked == data['is_locked'])
    except:
        print("no locked projects")

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

    print(tmp_project.all())
    return tmp_project.all(), 201


def save_changes(data: Project) -> None:
    db.session.add(data)
    db.session.commit()


@jwt_required()
def update_a_project(id):
    operator_id = get_jwt_identity()
    operator_role = list(db.session.query(User.sysrole).filter_by(id=operator_id).first())[0]
    tmp_project = Project.query.filter_by(id=id).first()
    if operator_role == "sysrole" or operator_role == "client":
        if not tmp_project:
            return "no that project", 404
        if tmp_project.is_locked == True:
            return "project locked!", 401
        update_val = request.json
        print(update_val)
        projectname_exist = Project.query.filter(Project.project_name == update_val['project_name']).first()
        if projectname_exist and projectname_exist.id != int(id):
            return "conflict name!", 409
        # 如果有经理
        if update_val['project_manager_name']:
            if not User.query.filter(User.username == update_val['project_manager_name']).filter(
                    User.sysrole == "client").first():
                return f"no such manager!", 404
        wj2o(tmp_project, update_val)
        print(update_val)
        tmp_project.modified_time = datetime.now()
        save_changes(tmp_project)
        response_object = {
            'code': 'success',
            'message': f'project {id} updated!'.format()
        }
        details = " update project " + str(id)
        save_log("Modify", get_jwt_identity(), details)
        return response_object, 201
    else:
        return f"no permission", 401


def get_projects_by_org_id(id):
    projects = Project.query.filter_by(orgid=id).all()
    return projects, 201


def get_project_number():
    response_object = {
        'code': 'success',
        'number': Project.query.count()
    }
    return response_object, 200
