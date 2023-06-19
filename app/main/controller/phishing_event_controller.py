from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource

from app.main import db
from ..util.dto import Event_DTO
from ..service.phishing_event_service import *
from typing import Dict, Tuple

from ..util.file import upload_file
from ..util.response_tip import *
from ..util.write_json_to_obj import wj2o

ns = Event_DTO.ns
_PhishingEventIn = Event_DTO.phishing_event_in
_PhishingEventOut = Event_DTO.phishing_event_out
_event_Search = Event_DTO.searchIn

@ns.route('/')
class Phishingevents(Resource):

    @ns.doc('list_of_phishing_events')
    @ns.marshal_list_with(_PhishingEventOut, envelope='children')
    # @jwt_required
    def get(self):
        """展示所有的中招记录（👈）"""
        return get_all_events()

    @ns.expect(_PhishingEventIn, validate=True)
    @ns.response(201, 'Event successfully created.')
    @ns.doc('create a new phishing event')
    def post(self) -> Tuple[Dict[str, str], int]:
        """Creates a new Event """
        data = request.json
        return save_new_event(data=data)


@ns.route('/<id>')
@ns.param('id', 'The Phishing event identifier')
@ns.response(404, 'Phishing event not found.')
class Phishingevent(Resource):
    @ns.doc('get a phishing event')
    @ns.marshal_with(_PhishingEventOut)
    def get(self, id):
        """通过事件id获取一个中招记录"""
        event, http_code = get_a_event(id)
        if not event:
            ns.abort(404)
        else:
            return event


@ns.route('/search')
class SearchForEvents(Resource):
    """task view"""

    @ns.doc('search for phishing events')
    @ns.marshal_list_with(_PhishingEventOut, envelope='children')
    @ns.expect(_event_Search, validate=True)
    def post(self):
        """search for events by 中招人员id、中招任务id、捕获用服务器id、发送方服务器id"""
        data = request.json
        return search_for_events(data)

@ns.route('/receive/<int:uid>/<int:tid>')
class ReceiveEvent(Resource):
    """receive a phishing event"""

    @ns.doc('receive a phishing event')
    def post(self, uid, tid):
        event = {}
        event['type'] = 'email phishing'
        event['user_input'] = str(request.json)
        event['uid'] = uid
        event['task_id'] = tid
        event['catcher_id'] = 1
        event['server_id'] = 1

        return save_new_event(event)