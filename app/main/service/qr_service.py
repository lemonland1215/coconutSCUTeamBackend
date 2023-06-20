from app.main.model.mail_template import Mailtemplate
from datetime import datetime
from flask import request, Response
from app.main import db
from typing import Dict, Tuple
from flask_jwt_extended import get_jwt_identity, jwt_required
import qrcode
from zipfile import ZipFile
from io import BytesIO

from app.main.model.server_catcher import Servercatcher
from app.main.model.task import Task
from app.main.util.response_tip import *
from app.main.util.write_json_to_obj import wj2o

def qr_generate(tid):
    uid_list = [1, 2]
    img_bytes_list = []
    for uid in uid_list:
        url = 'http://10.133.29.27:5004/mail/2?uid='+str(uid)+'&tid='
        im = qrcode.make(url)
        img = BytesIO()
        im.save(img, format='PNG')
        img_bytes_list.append(img.getvalue())
    zip_buf = BytesIO()
    with ZipFile(zip_buf, 'w') as zip_file:
        for i, img_bytes in enumerate(img_bytes_list):
            img_filename = f'qrcode_{i + 1}.png'
            zip_file.writestr(img_filename, img_bytes)
    zip_buf.seek(0)  # 将文件指针移动到文件起始位置
    zip_data = zip_buf.getvalue()

    return Response(zip_data, mimetype='application/octet-stream', headers={
        'Content-Disposition': 'attachment; filename=qrcode.zip'
    })
