from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource
from werkzeug.datastructures import FileStorage

from app.main import db
from ..util.dto import Sender_DTO
from ..service.sender_service import *
from typing import Dict, Tuple

from ..util.file import upload_file
from ..util.response_tip import *
from ..util.write_json_to_obj import wj2o

ns = Sender_DTO.ns
_SenderIn = Sender_DTO.sender_in
_SenderOut = Sender_DTO.sender_out
_sender_Search = Sender_DTO.sender_search
_sender_Update = Sender_DTO.sender_update
_senderIDsIn = Sender_DTO.sender_eventIDsIn

@ns.route('/')
class Serversenders(Resource):

    @ns.doc('list_of_senders')
    @ns.marshal_list_with(_SenderOut, envelope='children')
    def get(self):
        """您可以在这里展示所有的sever sender"""
        return get_all_senders()

    @ns.expect(_SenderIn, validate=True)
    @ns.response(201, 'new sever sender successfully created.')
    @ns.doc('create a new sender')
    def post(self) -> Tuple[Dict[str, str], int]:
        """您可以在这里新建一个server sender"""
        data = request.json
        print("到达这里")
        return save_new_sender(data=data)

    @ns.doc('delete tasks')
    @ns.expect(_senderIDsIn, validate=True)
    def delete(self):
        """您可以在这里删除多个指定<id>的server sender"""
        senderIDsIn = request.json
        for id in senderIDsIn['id']:
            print(id)
            operate_a_sender(id, "delete")
        return response_with(SUCCESS_201)


@ns.route('/<id>')
@ns.param('id', 'The sender identifier')
@ns.response(404, 'Sever sender not found.')
class Serversender(Resource):
    @ns.doc('delete a sender')
    def delete(self, id):
        """您可以删除一个指定的sender"""
        sender, resp_status_code = get_a_sender(id)
        if not sender:
            ns.abort(404)
        else:
            return operate_a_sender(id, "delete")

    @ns.expect(_sender_Update, validate=True)
    @ns.response(201, 'Sever sender successfully modified.')
    @ns.doc("update a server sender's info")
    def put(self, id):
        """您可以在这里修改sever sender的一些info（不包括状态）"""
        return update_a_sender(id)

    @ns.doc('get a server sender')
    @ns.marshal_with(_SenderOut)
    def get(self, id):
        """get a server sender by its id"""
        sender, http_code = get_a_sender(id)
        if not sender:
            ns.abort(404)
        else:
            return sender

@ns.route('/action/<operator>')
@ns.param('operator', 'such as freeze|unfreeze, lock|unlock, delete etc')
@ns.response(404, 'Organization not found.')
class PatchSenders(Resource):
    """organization view"""

    @ns.doc('operate organizations')
    @ns.expect(_senderIDsIn, validate=True)
    def patch(self, operator):
        """您可以在这里修改server sender的状态"""
        senderIDs = request.json
        for id in senderIDs['id']:
            operate_a_sender(id, operator)
        return response_with(SUCCESS_201)

@ns.route('/search')
class SearchForSenders(Resource):
    """organization view"""

    @ns.doc('search for server senders')
    @ns.marshal_list_with(_SenderOut, envelope='children')
    @ns.expect(_sender_Search, validate=True)
    def post(self):
        """您可以在这里搜索以下内容：name|server|port|encryptalg|isfrozen|islocked"""
        data = request.json
        return search_for_senders(data)