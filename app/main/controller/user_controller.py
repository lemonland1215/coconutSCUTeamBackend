from app.main.util.dto import User_DTO
from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required
from app.main.service.user_service import save_new_user, get_a_user, get_all_users, get_users_by_org_id, \
    operate_a_user, search_for_user, update_a_user, delete_users, get_project_all_users, get_org_all_users
from typing import Dict, Tuple
from ..util.response_tip import *

ns = User_DTO.ns
_user_In = User_DTO.user_In
_user_Out = User_DTO.user_Out
_user_IDs_In = User_DTO.user_IDs_In
_user_Search = User_DTO.searchWordsIn
_user_Update = User_DTO.updateIn


# 对所有用户
@ns.route('/')
class UserList(Resource):
    @ns.doc('list_of_registered_users')
    # @admin_token_required
    @ns.marshal_list_with(_user_Out, envelope='children')
    def get(self):
        """List all registered users"""
        return get_all_users()

    # @jwt_required()
    @ns.expect(_user_In, validate=True)
    @ns.response(201, 'User successfully created.')
    @ns.doc('create a new user')
    def post(self) -> Tuple[Dict[str, str], int]:
        """Creates a new user """
        data = request.json
        return save_new_user(data=data)


    @ns.doc('delete all users')
    @jwt_required()
    @ns.response(201, 'Users deleted!')
    def delete(self):
        """Delete all users"""
        return delete_users()

@ns.route('/<id>/info')
@ns.param('id', 'The Project identifier')
class ProjectUser(Resource):
    @ns.doc('List all registered users')
    @ns.marshal_list_with(_user_Out, envelope='children')
    def get(self, id):
        """输出指定project<id>的所有用户(staff)"""
        return get_project_all_users(id)

@ns.route('/<name>/org/info')
@ns.param('name', 'The Org name')
class ProjectUser(Resource):
    @ns.doc('List all registered users by specific org name')
    @ns.marshal_list_with(_user_Out, envelope='children')
    def get(self, name):
        """输出指定organization<name>的所有用户(client)"""
        return get_org_all_users(name)

# 直接通过id查询
@ns.route('/<id>')
@ns.param('id', 'The User identifier')
@ns.response(404, 'User not found.')
class User(Resource):
    @ns.doc('get a user')
    @ns.marshal_with(_user_Out)
    def get(self, id):
        """get a user by its identifier"""
        user = get_a_user(id)
        if not user:
            ns.abort(404)
        else:
            return user

    @jwt_required()
    @ns.doc('update a user')
    @ns.response(201, 'User successfully modified.')
    @ns.expect(_user_Update, validate=True)
    def put(self, id):
        """update a user by its identifier"""
        # user = get_a_user(id)
        # if not user:
        #     return response_with(INVALID_INPUT_422)
        #
        # else:
        return update_a_user(id)

    # 没事别写乱七八糟的装饰器
    @jwt_required()
    @ns.doc('delete a user')
    def delete(self, id):
        """Delete a user by identifier"""
        user = get_a_user(id)
        if not user:
            ns.abort(404)
        else:
            return operate_a_user(id, "delete")


@ns.route('/<id>/action/<operator>')
@ns.param('operator', 'such as pause|restore, lock|unlock etc')
@ns.param('id', 'The users identifier')
@ns.response(404, 'User not found.')
class PatchUser(Resource):
    """user view"""
    @jwt_required()
    @ns.doc('modify a user')
    def patch(self, id, operator):
        """modify the status of users, status enum: lock|unlock"""
        user = get_a_user(id)
        if not user:
            ns.abort(404)
        else:
            return operate_a_user(id, operator)


@ns.route('/search')
@ns.response(404, 'User not found.')
class SearchForUsers(Resource):
    """user view"""
    @ns.doc('search_users')
    @ns.marshal_list_with(_user_In, envelope='children')
    @ns.expect(_user_Search, validate=True)
    def post(self):
        """search for users by id, partial_name, create_time, modify_time"""
        data = request.json
        return search_for_user(data)


# 通过公司查询
@ns.route('/organization/<id>')
@ns.param('id', 'The organization identifier')
@ns.response(404, 'Organization not found.')
class User(Resource):
    @ns.doc('get users by organization id')
    @ns.marshal_with(_user_Out, envelope='children')
    def get(self, id):
        """get a user given its identifier"""
        users, http_code = get_users_by_org_id(id)
        if not users:
            ns.abort(404)
        else:
            return users, 200