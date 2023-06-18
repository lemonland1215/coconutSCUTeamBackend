from flask import request, make_response, session, current_app, send_file, send_from_directory
from flask_restx import Resource
from flask_jwt_extended import jwt_required
from ..util.dto import File_DTO
from typing import Dict, Tuple

import os

ns = File_DTO.ns

@ns.route('/<path:filename>')
class File(Resource):
    """
        return a file to show
    """
    @ns.doc('return a file')
    def get(self, filename):
        print(filename)
        ''' show a file or image '''
        return send_from_directory("static/upload/", filename)