from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource
from werkzeug.datastructures import FileStorage

from app.main import db
from ..util.dto import Catcher_DTO
from ..service.catcher_service import *
from typing import Dict, Tuple

from ..util.file import upload_file
from ..util.response_tip import *
from ..util.write_json_to_obj import wj2o

ns = Catcher_DTO.ns
_CatcherIn = Catcher_DTO.catcher_in
_CatcherOut = Catcher_DTO.catcher_out
_catcher_Search = Catcher_DTO.catcher_search
_catcher_Update = Catcher_DTO.catcher_update
_catcherIDsIn = Catcher_DTO.catcherIDsIn

@ns.route('/')
class Servercatchers(Resource):

    @ns.doc('list_of_catchers')
    @ns.marshal_list_with(_CatcherOut, envelope='children')
    def get(self):
        """您可以在这里展示所有的sever catcher"""
        return get_all_catchers()

    @ns.expect(_CatcherIn, validate=True)
    @ns.response(201, 'new sever catcher successfully created.')
    @ns.doc('create a new catcher')
    def post(self) -> Tuple[Dict[str, str], int]:
        """您可以在这里新建一个server catcher"""
        data = request.json
        print("到达这里")
        return save_new_catcher(data=data)

    @ns.doc('delete tasks')
    @ns.expect(_catcherIDsIn, validate=True)
    def delete(self):
        """您可以在这里删除多个指定<id>的catcher sender"""
        catcherIDsIn = request.json
        for id in catcherIDsIn['id']:
            print(id)
            operate_a_catcher(id, "delete")
        return response_with(SUCCESS_201)


@ns.route('/<id>')
@ns.param('id', 'The catcher identifier')
@ns.response(404, 'Sever catcher not found.')
class Servercatcher(Resource):
    @ns.doc('delete a scatcher')
    def delete(self, id):
        """您可以删除一个指定的sender"""
        catcher, resp_status_code = get_a_catcher(id)
        if not catcher:
            ns.abort(404)
        else:
            return operate_a_catcher(id, "delete")

    @ns.expect(_catcher_Update, validate=True)
    @ns.response(201, 'Sever catcher successfully modified.')
    @ns.doc("update a server catcher's info")
    def put(self, id):
        """您可以在这里修改sever sender的一些info（不包括状态）"""
        return update_a_catcher(id)

    @ns.doc('get a server catcher')
    @ns.marshal_with(_CatcherOut)
    def get(self, id):
        """get a server sender by its id"""
        catcher, http_code = get_a_catcher(id)
        if not catcher:
            ns.abort(404)
        else:
            return catcher

@ns.route('/action/<operator>')
@ns.param('operator', 'such as freeze|unfreeze, lock|unlock, delete etc')
@ns.response(404, 'catcher not found.')
class PatchSenders(Resource):
    """catcher view"""

    @ns.doc('operate catchers')
    @ns.expect(_catcherIDsIn, validate=True)
    def patch(self, operator):
        """您可以在这里修改server catcher的状态"""
        catcherIDs = request.json
        for id in catcherIDs['id']:
            operate_a_catcher(id, operator)
        return response_with(SUCCESS_201)

@ns.route('/search')
class SearchForCatchers(Resource):
    """catcher view"""

    @ns.doc('search for server senders')
    @ns.marshal_list_with(_CatcherOut, envelope='children')
    @ns.expect(_catcher_Search, validate=True)
    def post(self):
        """您可以在这里搜索以下内容：name | server | port | isfrozen | islocked"""
        data = request.json
        return search_for_catchers(data)