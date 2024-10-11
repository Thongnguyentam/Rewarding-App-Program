from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from database.database import Base


class SysUser(Base):
    __tablename__ = "SYS_USER"
    id = Column(Integer, primary_key = True, index = True)
    username = Column(String(255))
    balance = Column(Integer)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), nullable=False)
    
class UserPayer(Base):
    __tablename__ = "USER_PAYER"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('SYS_USER.id'))
    payer_id = Column(Integer, ForeignKey('SYS_PAYER.id'))
    points = Column(Integer)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), nullable=False)