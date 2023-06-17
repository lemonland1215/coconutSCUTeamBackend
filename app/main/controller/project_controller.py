from app.main.util.dto import Project_DTO
from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required
from app.main.service.user_service import save_new_user, get_a_user, get_all_users, get_users_by_org_id, \
    operate_a_user, search_for_user, update_a_user
from app.main.service.project_service import save_new_project, get_a_project, get_all_projects, get_projects_by_org_id, \
    operate_a_project, search_for_project, update_a_project
from typing import Dict, Tuple
from ..util.response_tip import *

ns = Project_DTO.ns
_project_In = Project_DTO.project_In
_project_Out = Project_DTO.project_Out
_project_IDs_In = Project_DTO.project_IDs_In
_project_Search = Project_DTO.searchIn
_project_Update = Project_DTO.updateIn


@ns.route('/')
class ProjectList(Resource):
    @ns.doc('list_of_registered_projects')
    # @admin_token_required
    @ns.marshal_list_with(_project_Out, envelope='children')
    def get(self):
        """List all registered projects"""
        return get_all_projects()

    @jwt_required()
    @ns.expect(_project_In, validate=True)
    @ns.response(201, 'Project successfully created.')
    @ns.doc('create a new project')
    def post(self) -> Tuple[Dict[str, str], int]:
        """Creates a new project """
        data = request.json
        return save_new_project(data=data)


# 直接通过id查询
@ns.route('/<id>')
@ns.param('id', 'The projects identifier')
@ns.response(404, 'Project not found.')
class User(Resource):
    @ns.doc('get a project')
    @ns.marshal_with(_project_Out)
    def get(self, id):
        """get a project by its identifier"""
        project = get_a_project(id)
        if not project:
            return response_with(INVALID_INPUT_422)
        else:
            return project

    @jwt_required()
    @ns.doc('update a project')
    @ns.response(201, 'Project successfully modified.')
    @ns.expect(_project_Update, validate=True)
    def put(self, id):
        """update a project by its identifier"""
        # user = get_a_user(id)
        # if not user:
        #     return response_with(INVALID_INPUT_422)
        #
        # else:
        return update_a_project(id)

    # 没事别写乱七八糟的装饰器
    @jwt_required()
    @ns.doc('delete a project')
    def delete(self, id):
        """Delete a project by identifier"""
        project = get_a_project(id)
        if not project:
            ns.abort(404)
        else:
            return operate_a_project(id, "delete")


@ns.route('/<id>/action/<operator>')
@ns.param('operator', 'such as pause|restore, lock|unlock etc')
@ns.param('id', 'The projects identifier')
@ns.response(404, 'Project not found.')
class PatchProject(Resource):
    """project view"""
    @jwt_required()
    @ns.doc('modify a project')
    def patch(self, id, operator):
        """modify the status of projects, status enum: lock|unlock"""
        project = get_a_project(id)
        if not project:
            ns.abort(404)
        else:
            return operate_a_project(id, operator)


@ns.route('/search')
class SearchForProjects(Resource):
    """project view"""
    @ns.doc('search_projects')
    @ns.marshal_list_with(_project_In, envelope='children')
    @ns.expect(_project_Search, validate=True)
    def post(self):
        """search for projects by id, partial_name, create_time, modify_time"""
        data = request.json
        return search_for_project(data)


# 通过公司查询
@ns.route('/organization/<id>')
@ns.param('id', 'The organization identifier')
@ns.response(404, 'Organization not found.')
class Project(Resource):
    @ns.doc('get projects by organization id')
    @ns.marshal_with(_project_Out, envelope='children')
    def get(self, id):
        """get a project given its identifier"""
        projects, http_code = get_projects_by_org_id(id)
        if not projects:
            return response_with(INVALID_INPUT_422)
        else:
            return projects, 201
