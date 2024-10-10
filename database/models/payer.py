from sqlalchemy import Column, DateTime, Integer, String, func
from database.database import Base


class SysPayer(Base):
    __tablename__ = 'SYS_PAYER'
    id = Column(Integer, primary_key= True, index = True)
    name = Column(String(255))
    created_at = Column(DateTime, server_default = func.now(), nullable = False)