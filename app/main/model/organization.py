from .. import db
from datetime import datetime


class Organization(db.Model):
    __tablename__ = 't_organization'
    __table_args__ = {'comment': '部门表'}

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, comment='部门编号')
    name = db.Column(db.String(16), nullable=False, comment='部门名称')
    istoporg = db.Column(db.INT, nullable=False, comment='是否是顶级组织')
    higherorgid = db.Column(db.INTEGER, nullable=False, default=0, comment='上级部门编号;若已经为顶级单位，父级单位则为0')
    islocked = db.Column(db.BOOLEAN, nullable=False, comment='是否锁定')
    isfrozen = db.Column(db.BOOLEAN, nullable=False, comment='是否冻结')
    createdbyuid = db.Column(db.INTEGER, nullable=False, comment='创建人编号')
    createtime = db.Column(db.DateTime, nullable=False, default=datetime.now(), comment='创建时间')
    freezetime = db.Column(db.DateTime, comment='冻结时间')
    frozenbyuid = db.Column(db.INTEGER, comment='发起冻结的人编号')
    logopath = db.Column(db.String(255), comment='logo路径')
    comments = db.Column(db.String(5120), comment='备注')
    modifiedbyuid = db.Column(db.INTEGER, comment='发起修改的用户编号')
    modifytime = db.Column(db.DateTime, comment='修改时间')
    clientcontact = db.Column(db.String(16), nullable=False, comment='客户对接人')

    @staticmethod
    def init_db():
        org = Organization()
        org.name = '猫猫缝补公司'
        org.istoporg = 1
        org.higherorgid = 0
        org.islocked = 0
        org.isfrozen = 0
        org.createdbyuid = 1
        org.clientcontact = '喵喵喵'

        db.session.add(org)
        db.session.commit()

