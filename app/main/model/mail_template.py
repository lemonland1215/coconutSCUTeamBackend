from .. import db
from datetime import datetime


class Mailtemplate(db.Model):
    __tablename__ = 't_mail_template'
    __table_args__ = {'comment': '邮件模板表'}

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, comment='邮件编号')
    subject = db.Column(db.String(255), nullable=False, comment='邮件主题')
    type = db.Column(db.String(50), nullable=False, comment='邮件类型： text|html|doc|md|excel')
    content = db.Column(db.String(50000), nullable=False, comment='邮件内容')
    attach_id = db.Column(db.INTEGER, comment='附件id')
    createdbyuid = db.Column(db.INTEGER, nullable=False, comment='创建人编号')
    createtime = db.Column(db.DateTime, nullable=False, default=datetime.now(), comment='创建时间')
    modifybyuid = db.Column(db.INTEGER, comment='修改人编号')
    modifytime = db.Column(db.DateTime, comment='修改时间')
    comments = db.Column(db.String(5120), comment='备注')
    islocked = db.Column(db.BOOLEAN, nullable=False, comment='是否锁定')
    lockbyuid = db.Column(db.INTEGER, comment='发起锁定的人编号')
    locktime = db.Column(db.DateTime, comment='锁定时间')

    @staticmethod
    def init_db():
        mail = Mailtemplate()
        mail.subject = '测试'
        mail.type = 'text'
        mail.content = "！！！本邮件仅作测试用！！！<br>亲爱的{{ user.name }}：<br>&" \
                       "nbsp;&nbsp;&nbsp;&nbsp;ChatGPT中文免费版现已推出！CloseAI为黄钻会员推出了GPT-100免费使用权" \
                       "<br>点击访问申请使用权！→<a href='http://server/?id={{ user.id }}'>http://closeai.chat.com/" \
                       "</a><br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" \
                       "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;喵喵公司"
        mail.createdbyuid = 1
        mail.islocked = 0
        db.session.add(mail)
        db.session.commit()

