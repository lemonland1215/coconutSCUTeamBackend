# 模型部分代码
from .. import db, flask_bcrypt
from datetime import datetime


class Project(db.Model):
    """ Project Model for storing user related details """
    __tablename__ = 't_project'
    id = db.Column(db.INTEGER, primary_key=True, comment='项目编号')
    projectname = db.Column(db.String(100), nullable=False, unique=True, comment='项目名称')
    project_manager_id = db.Column(db.INTEGER, nullable=False, comment='项目管理员id')
    project_creator_id = db.Column(db.INTEGER, nullable=False, comment='项目创建人id')
    orgid = db.Column(db.INTEGER, nullable=False, comment='客户公司id')
    # orgname = db.Column(db.String(100), nullable=False, comment='客户公司名称')
    customer_contact = db.Column(db.String(50), nullable=True, default='unknown', comment='客户对接人')
    contact_email = db.Column(db.String(100), nullable=True, default='unknown', comment='对接人邮箱')
    liaison_id = db.Column(db.INTEGER, nullable=False, comment='项目联系人编号')
    test_number = db.Column(db.INTEGER, nullable=True, default=0, comment='项目测评次数')
    comment = db.Column(db.String(256), nullable=True, default='comment', comment='备注')
    modified_time = db.Column(db.DateTime, nullable=True, default=datetime.now(), comment='修改时间')
    is_locked = db.Column(db.BOOLEAN, nullable=False, default=False, comment='是否锁定')
    locked_by = db.Column(db.INTEGER, nullable=True, default=-1, comment='锁定者编号')
    locked_time = db.Column(db.DateTime, nullable=True, comment='锁定时间')
    is_frozen = db.Column(db.BOOLEAN, nullable=False, default=False, comment='是否被冻结')
    frozen_by = db.Column(db.INTEGER, nullable=True, default=-1, comment='冻结者编号')
    frozen_time = db.Column(db.DateTime, nullable=True, comment='冻结时间')
    status = db.Column(db.String(50), nullable=False, default='Running', comment='项目进展状态：Running|Stop|Pause|Finish')
    create_time = db.Column(db.DateTime, default=datetime.now(), nullable=False, comment='创建时间')
    end_time = db.Column(db.DateTime, nullable=True, comment='结束时间')


    @staticmethod
    def init_db():
        project = Project()
        project.projectname = 'stafelring'
        project.project_manager_id = 2
        project.project_creator_id = 1
        project.orgid = 1
        project.customer_contact = 'stdlring'
        project.contact_email = 'mail@mail'
        project.liaison_id = 1
        project.is_locked = 0
        project.is_frozen = 0
        project.status = 'Running'
        db.session.add(project)
        db.session.commit()
