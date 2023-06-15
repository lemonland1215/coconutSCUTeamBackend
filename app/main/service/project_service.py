from flask import request
from app.main import db
from app.main.model.project import Project
from typing import Dict, Tuple
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.main.util.write_json_to_obj import wj2o
from datetime import datetime


@jwt_required()
def save_new_project(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    project = Project.query.filter_by(email=data['email']).first()
    if not project:
        new_project = project()
        data = request.json
        wj2o(new_project, data)
        save_changes(new_project)
        return generate_token(new_project)
    else:
        response_object = {
            'status': 'fail',
            'message': 'project already exists. Please Log in.',
        }
        return response_object, 409


def get_all_projects():
    return Project.query.all()


def get_a_project(id):
    return Project.query.filter_by(id=id).first()


def generate_token(project: Project) -> Tuple[Dict[str, str], int]:
    try:
        # generate the auth token
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': create_access_token(project.id)
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.' + str(e)
        }
        return response_object, 401


def get_projects_by_org_id(id):
    projects = Project.query.filter_by(orgid=id).all()
    return projects, 201


@jwt_required()
def operate_a_project(id, operator):
    tmp_project = Project.query.filter_by(id=id).first()
    if not tmp_project:
        return "ITEM_NOT_EXISTS", 404
    if tmp_project.is_locked:
        if operator != "unlock":
            return "ITEM_LOCKED", 401
        else:
            tmp_project.is_locked = False
    else:
        if operator == "lock":
            tmp_project.is_locked = True
        elif operator == "delete":
            db.session.delete(tmp_project)
        elif operator == "freeze":
            tmp_project.is_frozen = True
            tmp_project.frozen_time = datetime.now()
            tmp_project.frozen_by = get_jwt_identity()
        elif operator == "unfreeze":
            tmp_project.is_frozen = False
            tmp_project.frozen_time = None
            tmp_project.frozen_by = None
        else:
            print("什么东西")
            return "INVALID_INPUT", 422
    db.session.commit()
    response_object = {
        'code': 'success',
        'message': f'project {id} updated!'.format()
    }
    return response_object, 201


def search_for_project(data):
    tmp_project = Project.query
    try:
        if data['id']:
            print(data['id'])
            tmp_project = tmp_project.filter_by(id=data['id'])
    except:
        print("无id")

    try:
        if data['projectname']:
            tmp_project = tmp_project.filter(Project.projectname.like("%" + data['projectname'] + "%"))
    except:
        print("无name")

    try:
        if data['sysrole']:
            tmp_project = tmp_project.filter(Project.sysrole.like("%" + data['sysrole'] + "%"))
    except:
        print("无sysrole")

    try:
        if data['is_frozen']:
            tmp_project = tmp_project.filter_by(is_frozen=data['is_frozen'])
    except:
        print("无status")

    try:
        if data['orgid']:
            tmp_project = tmp_project.filter_by(orgid=data['orgid'])
    except:
        print("无orgid")

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
        return "book record locked!", 401
    update_val = request.json
    # update_val['lastmodifiedbyuid'] = get_jwt_identity()
    wj2o(tmp_project, update_val)
    tmp_project.modified_time = datetime.now()
    save_changes(tmp_project)
    response_object = {
        'code': 'success',
        'message': f'project {id} updated!'.format()
    }
    return response_object, 201
