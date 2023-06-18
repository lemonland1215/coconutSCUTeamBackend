# 模型部分代码
from .. import db, flask_bcrypt
from datetime import datetime


class Liaison(db.Model):
    """ Liaison Model for storing user related details """
    __tablename__ = 't_liaison'
    liaison_id = db.Column(db.INTEGER, primary_key=True, nullable=False, comment='联系人编号')
    liaison_name = db.Column(db.String(50), nullable=False, comment='项目联系人名称')
    liaison_email = db.Column(db.String(100), nullable=False, comment='项目联系人邮箱')