from flask import request, make_response, session, current_app, send_from_directory
from flask_restx import Resource
from flask_jwt_extended import jwt_required
from ..util.dto import QR_DTO
from typing import Dict, Tuple
from ..service.qr_service import *

import os

ns = QR_DTO.ns

@ns.route('/<int:tid>')
class Qrcode(Resource):
    """
        return qrcode to download
    """
    @ns.doc('return qrcode')
    def get(self, tid):
        """show qrcode"""
        return qr_generate(tid)