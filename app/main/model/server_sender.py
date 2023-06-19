from .. import db
from datetime import datetime


class Serversender(db.Model):
    __tablename__ = 't_server_sender'
    __table_args__ = {'comment': '发送方服务器'}

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, comment='发送方服务器编号')
    name = db.Column(db.String(50), nullable=False, comment='发送方服务器名称')
    server = db.Column(db.String(15),nullable=False, comment='IP地址')
    port = db.Column(db.INTEGER, nullable=False, comment='端口号')
    encryptalg = db.Column(db.String(50), nullable=False, comment='加密算法')
    password = db.Column(db.String(50), nullable=False, comment='密码')
    islocked = db.Column(db.BOOLEAN, nullable=False, comment='是否锁定')
    isfrozen = db.Column(db.BOOLEAN, nullable=False, comment='是否冻结')
    createdbyuid = db.Column(db.INTEGER, nullable=False, comment='创建人编号')
    createtime = db.Column(db.DateTime, nullable=False, default=datetime.now(), comment='创建时间')
    freezetime = db.Column(db.DateTime, comment='冻结时间')
    frozenbyuid = db.Column(db.INTEGER, comment='发起冻结的人编号')
    modifiedbyuid = db.Column(db.INTEGER, comment='发起修改的用户编号')
    modifytime = db.Column(db.DateTime, comment='修改时间')
    comments = db.Column(db.String(5120), comment='备注')
    lockbyuid = db.Column(db.INTEGER,comment='发起锁定的人编号')
    locktime = db.Column(db.DateTime, comment='锁定时间')

    @staticmethod
    def init_db():
        sender = Serversender()
        sender.name = 'xiancaoro'
        sender.server = '127.0.0.1'
        sender.port = 50
        sender.encryptalg = 'AES'
        sender.password = 'kkkkk'
        sender.islocked = 0
        sender.isfrozen = 0
        sender.createdbyuid = 1

        db.session.add(sender)
        db.session.commit()