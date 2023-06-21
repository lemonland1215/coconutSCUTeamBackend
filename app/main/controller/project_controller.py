from app.main.util.dto import Project_DTO
from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required
from app.main.service.project_service import save_new_project, get_a_project, get_all_projects, get_projects_by_org_id, \
    operate_a_project, search_for_project, update_a_project, delete_projects, get_project_number
from typing import Dict, Tuple
from app.main.util.response_tip import *

ns = Project_DTO.ns
_project_In = Project_DTO.project_In
_project_Out = Project_DTO.project_Out
_project_IDs_In = Project_DTO.project_IDs_In
_project_Search = Project_DTO.searchIn
_project_Update = Project_DTO.updateIn


@ns.route('/')
class ProjectList(Resource):
    @ns.doc('list_of_created_projects')
    # @admin_token_required
    @ns.marshal_list_with(_project_Out, envelope='children')
    def get(self):
        """List all created projects"""
        return get_all_projects()

    # @ns.doc('get_all_project_ids')
    # def get(self):
    #     """您可以在这里查看已有的project的id"""
    #     return get_all_project_ids()

    @jwt_required()
    @ns.expect(_project_In, validate=True)
    @ns.response(201, 'Project successfully created.')
    @ns.doc('create a new project')
    def post(self) -> Tuple[Dict[str, str], int]:
        """Creates a new project """
        data = request.json
        return save_new_project(data=data)

    @jwt_required()
    @ns.doc('delete selected projects')
    @ns.response(201, 'Projects deleted!')
    @ns.expect(_project_IDs_In, validate=True)
    def delete(self):
        """Delete selected projects"""
        projectIDs = request.json
        for id in projectIDs['id']:
            operate_a_project(id, "delete")
        return response_with(SUCCESS_201)


@ns.route('/statistics')
class Statistics(Resource):
    @ns.doc('Get project number')
    def get(self):
        """ Get project number """
        return get_project_number()


# 直接通过id查询
@ns.route('/<id>')
@ns.param('id', 'The projects identifier')
@ns.response(404, 'Project not found.')
class Project(Resource):
    @ns.doc('get a project')
    @ns.marshal_with(_project_Out)
    def get(self, id):
        """get a project by its identifier"""
        project = get_a_project(id)
        if not project:
            ns.abort(404)
        else:
            return project

    # 没事别写乱七八糟的装饰器
    @jwt_required()
    @ns.doc('delete a project')
    def delete(self, id):
        """Delete a project by identifier"""
        return operate_a_project(id, "delete")

    @jwt_required()
    @ns.doc('update a project')
    @ns.response(201, 'Project successfully modified.')
    @ns.expect(_project_Update, validate=True)
    def put(self, id):
        """Update a project by its identifier"""
        return update_a_project(id)


@ns.route('/<id>/action/<operator>')
@ns.param('operator', 'such as pause|restore, lock|unlock etc')
@ns.param('id', 'The projects identifier')
@ns.response(404, 'Project not found.')
class PatchProject(Resource):
    """project view"""

    @jwt_required()
    @ns.doc('modify a project')
    def patch(self, id, operator):
        """Modify the status of projects, status enum: lock|unlock"""
        return operate_a_project(id, operator)


@ns.route('/search')
class SearchForProjects(Resource):
    """project view"""

    @ns.doc('search_projects')
    @ns.marshal_list_with(_project_Out, envelope='children')
    @ns.expect(_project_Search, validate=True)
    def post(self):
        """Search for projects by id, partial_name, create_time, modify_time"""
        data = request.json
        return search_for_project(data)

# # 通过公司查询
# @ns.route('/organization/<id>')
# @ns.param('id', 'The organization identifier')
# @ns.response(404, 'Organization not found.')
# class Project(Resource):
#     @ns.doc('get projects by organization id')
#     @ns.marshal_with(_project_Out, envelope='children')
#     def get(self, id):
#         """get a project given its identifier"""
#         projects, http_code = get_projects_by_org_id(id)
#         if not projects:
#             return response_with(INVALID_INPUT_422)
#         else:
#             return projects, 201
