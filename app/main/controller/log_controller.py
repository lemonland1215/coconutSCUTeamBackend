from app.main.util.dto import Log_DTO
from flask import request
from flask_restx import Resource
from app.main.service.log_service import get_all_logs, get_a_log
from typing import Dict, Tuple


ns = Log_DTO.ns
_log_Out = Log_DTO.log_Out
_log_search = Log_DTO.log_Search

@ns.route('/')
class LogList(Resource):
    @ns.doc('list_of_logs')
    @ns.marshal_list_with(_log_Out, envelope='children')
    def get(self):
        """List all logs"""
        return get_all_logs()


@ns.route('/<id>')
class ALog(Resource):
    @ns.doc('get a log')
    @ns.marshal_list_with(_log_Out, envelope='children')
    def get(self, id):
        """Get a log"""
        log = get_a_log(id)
        if not log:
            ns.abort(404)
        else:
            return get_a_log(id)