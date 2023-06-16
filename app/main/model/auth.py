from .. import db,jwt
from datetime import datetime

  
class TokenBlocklist(db.Model):
    # __bind_key__ = 'second_db'
    __tablename__ = 't_tokenblacklist'
    __table_args__ = {'comment': 'token黑名单'}

    id = db.Column(db.Integer, primary_key=True,  autoincrement=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)

