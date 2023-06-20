from .. import db
from datetime import datetime


class Servercatcher(db.Model):
    __tablename__ = 't_server_catcher'
    __table_args__ = {'comment': '捕获用服务器'}

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, comment='捕获用服务器编号')
    name = db.Column(db.String(50), nullable=False, comment='捕获用服务器名称')
    server = db.Column(db.String(15),nullable=False, comment='IP地址')
    port = db.Column(db.INTEGER, nullable=False, comment='端口号')
    status = db.Column(db.String(50),nullable=False, default='open', comment='捕获服务器状态：open | close | busy')
    islocked = db.Column(db.BOOLEAN, nullable=False, comment='是否锁定')
    isfrozen = db.Column(db.BOOLEAN, nullable=False, comment='是否冻结')
    createdbyuid = db.Column(db.INTEGER, nullable=False, comment='创建人编号')
    createtime = db.Column(db.DateTime, nullable=False, default=datetime.now(), comment='创建时间')
    freezetime = db.Column(db.DateTime, comment='冻结时间')
    frozenbyuid = db.Column(db.INTEGER, comment='发起冻结的人编号')
    modifiedbyuid = db.Column(db.INTEGER, comment='发起修改的用户编号')
    modifytime = db.Column(db.DateTime, comment='修改时间')
    lockbyuid = db.Column(db.INTEGER, comment='发起锁定的人编号')
    locktime = db.Column(db.DateTime, comment='锁定时间')
    comments = db.Column(db.String(5120), comment='备注')


    @staticmethod
    def init_db():
        catcher = Servercatcher()
        catcher.name = 'ran'
        catcher.server = '192.168.43.76'
        catcher.port = 5004
        catcher.islocked = 0
        catcher.isfrozen = 0
        catcher.createdbyuid = 1

        db.session.add(catcher)
        db.session.commit()