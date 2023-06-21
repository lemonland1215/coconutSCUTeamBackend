from app.main.util.dto import Statistics_DTO
from flask import request
from flask_restx import Resource
from app.main.service.statistics_service import *

ns = Statistics_DTO.ns

@ns.route('/')
class Statistics(Resource):
    @ns.doc('list of all statistics')
    def get(self):
        """List all statistics"""
        return get_statistics()
