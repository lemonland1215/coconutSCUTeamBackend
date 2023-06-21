from app.main.model.mail_template import Mailtemplate
from datetime import datetime
from flask import request, Response
from app.main import db
from typing import Dict, Tuple
from flask_jwt_extended import get_jwt_identity, jwt_required
import qrcode
from zipfile import ZipFile
from io import BytesIO
import json

from app.main.model.server_catcher import Servercatcher
from app.main.model.task import Task
from app.main.model.server_catcher import Servercatcher
from app.main.util.response_tip import *
from app.main.util.write_json_to_obj import wj2o

def get_a_task_users(tid):
    tem_task = Task.query.filter_by(id=tid).first()
    u_list = json.loads(tem_task.target_id_list)
    return u_list

def get_a_task_catcher(tid):
    tem_task = Task.query.filter_by(id=tid).first()
    catcher_id = tem_task.catcher_id
    print(catcher_id)
    tem_catcher = Servercatcher.query.filter_by(id=catcher_id).first()
    server = tem_catcher.server
    port = tem_catcher.port
    return 'http://'+server+':'+str(port)

def get_task_mail_id(tid):
    tem_task = Task.query.filter_by(id=tid).first()
    return tem_task.mail_id

def qr_generate(tid):
    uid_list = get_a_task_users(tid)
    img_bytes_list = []
    prefix = get_a_task_catcher(tid)
    mailid = get_task_mail_id(tid)

    for uid in uid_list:
        url = prefix + '/mail/' + str(mailid) + '?uid=' + str(uid) + '&tid=' + str(tid)
        im = qrcode.make(url)
        img = BytesIO()
        im.save(img, format='PNG')
        img_bytes_list.append(img.getvalue())
    zip_buf = BytesIO()
    with ZipFile(zip_buf, 'w') as zip_file:
        for i, img_bytes in enumerate(img_bytes_list):
            img_filename = f'qrcode_{uid_list[i]}.png'
            zip_file.writestr(img_filename, img_bytes)
    zip_buf.seek(0)  # 将文件指针移动到文件起始位置
    zip_data = zip_buf.getvalue()

    return Response(zip_data, mimetype='application/octet-stream', headers={
        'Content-Disposition': 'attachment; filename=qrcode_task_'+str(tid)+'.zip'
    })
