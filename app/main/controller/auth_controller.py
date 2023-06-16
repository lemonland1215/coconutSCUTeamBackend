from io import BytesIO
from pprint import pprint

from flask import request, send_file, make_response, session, current_app
from flask_restx import Resource
from flask_jwt_extended import jwt_required
from app.main.service.auth_helper import Auth
from ..util.dto import AuthDTO
from typing import Dict, Tuple

ns = AuthDTO.ns
auth_dto = AuthDTO.auth_dto


@ns.route('/login')
class UserLogin(Resource):
    """
        User Login Resource
    """
    @ns.doc('user login')
    @ns.expect(auth_dto, validate=True)
    def post(self) -> Tuple[Dict[str, str], int]:
        # get the post data
        data = request.json
        # with current_app.app_context():
        #     response = Auth.login_user(data=data,session=session)
        # print("login-seesion",session['verify_code'])
        return Auth.login_user(data=data,session=session)

@ns.route('/verify_code')
class GetVerifyCode(Resource):
    """
    Logout Resource
    """
    def get(self) -> Tuple[Dict[str, str], int]:
        """
            get a image verify code
        Returns:

        """
        image, code = Auth.generate_verify_code()
        # 图片以二进制形式写入
        buf = BytesIO()
        image.save(buf, 'jpeg')
        buf_str = buf.getvalue()
        # 把buf_str作为response返回前端，并设置首部字段
        response = make_response(buf_str)
        response.headers['Content-Type'] = 'image/gif'
        # 将验证码字符串储存在session中
        pprint(request.cookies)
        session['verify_code'] = code
        print("生成的验证码：", code)
        print("会话：",session['verify_code'])
        return response

@ns.route('/logout')
class UserLogout(Resource):
    """
    User Logout Resource
    """
    @ns.doc('user logout')
    # @jwt_required
    def delete(self) -> Tuple[Dict[str, str], int]:
        auth_info = request.headers.get('Authorization')
        print("*********************************")
        print("header",request.headers)
        print("auth_info",auth_info)
        return Auth.logout_user(auth_info)