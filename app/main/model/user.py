# 模型部分代码
from .. import db, flask_bcrypt
from datetime import datetime


class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = 't_user'
    # __table_args__ = {'comment': '用户表'}

    id = db.Column(db.INTEGER, primary_key=True, comment='用户编号')
    username = db.Column(db.String(16), nullable=False, comment='用户名')
    password_hash = db.Column(db.String(100), comment='密码hash')
    orgid = db.Column(db.INTEGER, comment='所属机构编号')
    sysrole = db.Column(db.String(255), nullable=False,
                        comment='系统角色：sysadmin | logadmin | projectadmin | projectowner')
    email = db.Column(db.String(255), unique=True, nullable=False, comment='邮箱')
    comment = db.Column(db.String(50), comment='备注')
    is_locked = db.Column(db.BOOLEAN, default=False, comment='是否锁定')
    is_frozen = db.Column(db.BOOLEAN, default=False, comment='是否被冻结')
    frozen_by = db.Column(db.INTEGER, comment='冻结者编号')
    frozen_time = db.Column(db.DateTime, comment='冻结时间')
    create_time = db.Column(db.DateTime, default=datetime.now(), nullable=False, comment='创建时间')
    modified_time = db.Column(db.DateTime, comment='修改时间')

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User '{}'>".format(self.username)

    # @staticmethod
    # def init_db():
    #     rets = [
    #         ('SixteenNight', 'A company', 'sysadmin', 'password', )
    #     ]
    #     for ret in rets:
    #         user = User()
    #         user.user_name = ret[0]
    #         user.orgid = ret[1]
    #         user.sysrole = ret[2]
    #         user.password_hash = hash(ret[3])
    #         db.session.add(user)
    #     db.session.commit()
