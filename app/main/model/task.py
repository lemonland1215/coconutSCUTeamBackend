from .. import db
from datetime import datetime


class Task(db.Model):
    __tablename__ = 't_task'
    __table_args__ = {'comment': '评测任务表'}

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, comment='任务编号')
    name = db.Column(db.String(16), nullable=False, comment='任务名称')
    project_id =  db.Column(db.INTEGER, nullable=False, comment='所属项目id')
    type = db.Column(db.String(16), nullable=False, comment='任务类型')
    mail_id = db.Column(db.INTEGER, nullable=False, comment='邮件模板id')
    comments = db.Column(db.String(5120), comment='备注')
    status = db.Column(db.String(16), nullable=False, comment='任务状态：Continue|Freeze|Pause|Finish')
    cacher_id = db.Column(db.INTEGER, nullable=False, comment='捕获服务器id')
    cacher_name = db.Column(db.String(16), nullable=False, comment='捕获服务器名称')
    report_status = db.Column(db.BOOLEAN, nullable=False, comment='报告是否生成')
    report_path = db.Column(db.String(50), nullable=False, comment='报告路径')
    target_num = db.Column(db.INTEGER, nullable=False, comment='目标人数')
    target_id_list = db.Column(db.ARRAY(db.INTEGER), nullable=False, comment='目标id列表')
    delivery_name = db.Column(db.String(16), nullable=False, comment='发件人名称')
    delivery_address = db.Column(db.String(255), nullable=False, comment='发件地址')
    delivery_time = db.Column(db.DateTime, nullable=False, comment='发件时间')
    delivery_freq = db.Column(db.INTEGER, nullable=False, comment='邮件发送频率(s)')
    mail_server_id = db.Column(db.INTEGER, nullable=False, comment='邮件服务器id')
    mail_server_name = db.Column(db.String(50), nullable=False, comment='邮件服务器名称')
    islocked = db.Column(db.BOOLEAN, nullable=False, comment='是否锁定')
    isfrozen = db.Column(db.BOOLEAN, nullable=False, comment='是否冻结')
    ispaused = db.Column(db.BOOLEAN, nullable=False, comment='是否暂停')
    createdbyuid = db.Column(db.INTEGER, nullable=False, comment='创建人编号')
    createtime = db.Column(db.DateTime, nullable=False, default=datetime.now(), comment='创建时间')
    freezetime = db.Column(db.DateTime, comment='冻结时间')
    frozenbyuid = db.Column(db.INTEGER, nullable=False, comment='发起冻结的人编号')
    pausetime = db.Column(db.DateTime, comment='暂停时间')
    pausebyuid = db.Column(db.INTEGER, nullable=False, comment='发起暂停的人编号')
    modifybyuid = db.Column(db.INTEGER, nullable=False, comment='修改人编号')
    modifytime = db.Column(db.DateTime, nullable=False, comment='修改时间')
    
