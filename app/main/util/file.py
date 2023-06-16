import os
from flask import request, url_for, send_file
from werkzeug.utils import secure_filename
from flask import current_app
import uuid

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'txt', 'zip', 'rar', 'docx', 'xlsx', 'pptx', 'wps'}


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file(subdir):
    """
    获取一个文件上传
    Params:
        file: 上传文件的名称
    Returns:
        json
    """
    file = request.files['file']
    # 校验文件名称合法
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename = random_filename(filename)
        upload_folder = os.path.join(current_app.config["UPLOAD_FOLDER"], subdir)
        file.save(os.path.join(upload_folder, filename))
        return {
            'msg': 'success',
            'url': "/".join(["upload", subdir, filename]),
        }
    else:
        return {
            'msg': '文件格式不支持'
        }


def random_filename(filename):
    ext = os.path.splitext(filename)[-1]
    print(filename)
    print("=======================>" + ext)
    new_filename = uuid.uuid4().hex + ext
    return new_filename
