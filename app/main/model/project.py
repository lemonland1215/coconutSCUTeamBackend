# 模型部分代码
from .. import db, flask_bcrypt
from datetime import datetime


class Project(db.Model):
    """ Project Model """
    __tablename__ = 't_project'
    id = db.Column(db.INTEGER, primary_key=True, comment='项目编号')
    project_name = db.Column(db.String(100), nullable=False, unique=True, comment='项目名称')
    client_id = db.Column(db.INTEGER, nullable=False, comment='甲方项目负责人id，兼任甲方联系人、管理员')
    project_creator_id = db.Column(db.INTEGER, nullable=False, comment='项目创建人id，兼任项目创建人、乙方项目管理员、联系人')
    orgid = db.Column(db.INTEGER, nullable=False, comment='客户公司id')
    comment = db.Column(db.String(256), nullable=True, default='comment', comment='备注')
    modified_time = db.Column(db.DateTime, nullable=False, default=datetime.now(), comment='修改时间')
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now(), comment='创建时间')
    end_time = db.Column(db.DateTime, nullable=True, comment='结束时间')
    is_locked = db.Column(db.BOOLEAN, nullable=False, default=False, comment='是否锁定')
    locked_by = db.Column(db.INTEGER, nullable=True, comment='锁定者编号')
    locked_time = db.Column(db.DateTime, nullable=True, comment='锁定时间')
    is_frozen = db.Column(db.BOOLEAN, nullable=False, default=False, comment='是否被冻结')
    frozen_by = db.Column(db.INTEGER, nullable=True, comment='冻结者编号')
    frozen_time = db.Column(db.DateTime, nullable=True, comment='冻结时间')
    status = db.Column(db.String(50), nullable=False, default='Running', comment='项目进展状态：Running|Frozen|Finish')

    @staticmethod
    def init_db():
        project = Project()
        project.project_name = 'stafelring'
        project.client_id = 1
        project.project_creator_id = 1
        project.orgid = 1
        db.session.add(project)
        db.session.commit()
