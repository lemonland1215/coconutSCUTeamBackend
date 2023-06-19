from .. import db
from datetime import datetime


class Phishingevent(db.Model):
    __tablename__ = 't_phishing_event'
    __table_args__ = {'comment': '中招事件记录'}

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, comment='中招事件编号')
    type = db.Column(db.String(50), nullable=False, comment='中招事件类型')
    user_input = db.Column(db.String(50000), nullable=False, comment='用户输入内容')
    time = db.Column(db.DateTime, nullable=False, comment='中招时间')
    uid = db.Column(db.INTEGER, nullable=False, comment='中招人员id')
    # uname = db.Column(db.String(50), nullable=False, comment='中招人员名称')
    task_id = db.Column(db.INTEGER, nullable=False, comment='中招任务id')
    catcher_id = db.Column(db.INTEGER, nullable=False, comment='捕获用服务器id')
    server_id = db.Column(db.INTEGER, nullable=False, comment='发送方服务器id')