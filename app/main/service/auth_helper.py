from pprint import pprint

from datetime import datetime, timedelta, timezone
from flask import request, session
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt
from app.main.model.user import User
from app.main.model.auth import TokenBlocklist
from app.main import *
from typing import Dict, Tuple
import random
import string
from PIL import Image, ImageFont, ImageDraw, ImageFilter

from app.main.util.response_tip import *


def rnd_color():
    """随机颜色"""
    return random.randint(32, 127), random.randint(32, 127), random.randint(32, 127)


def gen_text():
    """生成4位验证码"""
    return ''.join(random.sample(string.ascii_lowercase + string.digits, 4))


def draw_lines(draw, num, width, height):
    """划线"""
    for num in range(num):
        x1 = random.randint(0, width / 2)
        y1 = random.randint(0, height / 2)
        x2 = random.randint(0, width)
        y2 = random.randint(height / 2, height)
        draw.line(((x1, y1), (x2, y2)), fill='black', width=1)

def save_token(resp):
    # jti = get_jwt()["jti"]
    jti = resp
    now = datetime.now(timezone.utc)
    print("jti",jti,"now",now)
    db.session.add(TokenBlocklist(jti=jti, created_at=now))
    db.session.commit()

class Auth:
    @staticmethod
    def generate_verify_code():
        """生成验证码图形"""
        code = gen_text()
        # 图片大小120×50
        width, height = 120, 50
        # 新图片对象
        img = Image.new('RGB', (width, height), 'white')
        # 字体
        font = ImageFont.truetype('app/static/arial.ttf', 40)
        # draw对象
        draw = ImageDraw.Draw(img)
        # 绘制字符串
        for item in range(4):
            draw.text((5 + random.randint(-3, 3) + 23 * item, 5 + random.randint(-3, 3)),
                      text=code[item], fill=rnd_color(), font=font)
        # 划线
        draw_lines(draw, 2, width, height)
        # 高斯模糊
        img = img.filter(ImageFilter.GaussianBlur(radius=1.5))
        return img, code

    @staticmethod
    def login_user(data: Dict[str, str], session) -> Tuple[Dict[str, str], int]:
        try:
            pprint(request.json)
            print("session--verify_code: ",session['verify_code'])
            # print("获取的生成的验证码：", session['verify_code'], ":", "发送来的验证码：", request.json['verify_code'])
            if session['verify_code'] != request.json['verify_code']:
                Auth.generate_verify_code()
                response_object = {
                    'status': 'fail',
                    'message': 'verify code error',
                }
                return response_object, 403
            # fetch the user data
            user = User.query.filter_by(email=data.get('email')).first()
            if user and user.check_password(data.get('password')):
                auth_token = create_access_token(user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                if auth_token:
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'Authorization': auth_token
                    }
                    return response_object, 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'email or password does not match.'
                }
                return response_object, 401

        except Exception as e:
            print(e)
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return response_object, 500

    @staticmethod
    def logout_user(data: str) -> Tuple[Dict[str, str], int]:
        # data -> auth_info
        print("##################################")
        print("data",data)
        if data:
            auth_token = data.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            print("resp:",resp)
            # if isinstance(resp, str):
                # mark the token as blacklisted
            return save_token(resp)
            # else:
            #     response_object = {
            #         'status': 'fail',
            #         'message': resp
            #     }
            #     return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 403

