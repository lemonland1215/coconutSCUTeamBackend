from .. import db
from datetime import datetime
class Base(db.Model):
    __abstract__ = True

    # TODO: 所有字段检测：reqired， default内容
    id = db.Column(db.INTEGER, primary_key=True, comment='各类编号')
    name = db.Column(db.String(32), nullable=False, comment='各类名称')
    createtime = db.Column(db.DateTime, nullable=False, default=datetime.now(), comment='创建时间')
    createdbyuid = db.Column(db.INTEGER, nullable=False, comment='创建人编号')
    islocked = db.Column(db.BOOLEAN, default=False, comment="说明：是否锁定;锁定：不允许修改、删除。值：('locked', 'unlocked')")
    lockedby = db.Column(db.db.INTEGER, comment="说明：锁定者编号。值：(uid|'sys')")
    comments = db.Column(db.String(5120), comment='备注')
    lastmodifiedtime = db.Column(db.DateTime, comment='修改时间')
    lastmodifiedbyuid = db.Column(db.INTEGER, comment='修改人编号')