from .. import db, flask_bcrypt
from datetime import datetime


class Log(db.Model):
    """ Log Model"""
    __tablename__ = 't_log'
    id = db.Column(db.INTEGER, primary_key=True, comment='Log编号')
    type = db.Column(db.Sting(50), nullable=False, comment='Log类型：Error，Login，Logout，Create，Delete，Modify，Search，Targeted')
    operator_id = db.Column(db.INTEGER, nullable=False, comment='操作者id，如果是targeted的就是中招人id')
    role = db.Column(db.String(50), nullable=True, comment='操作者身份')
    details = db.Column(db.String(256), nullable=False, comment='具体操作')
    time = db.Column(db.DateTime, default=datetime.now(), nullable=False, comment='Log记录时间')
    # example: 1 delete 2 admin 2023-6-19 'yyq delete organization 5'