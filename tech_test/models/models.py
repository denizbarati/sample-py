from tech_test.models.database import Base
from sqlalchemy import Column, Integer, String


class UserModel(Base):
    __tablename__ = 'users'
    # _id = Column(Integer, primary_key=True)
    username = Column(String, primary_key=True, unique=True)
    password = Column(String)
    name = Column(String)
    familyname = Column(String)
    
    
class UserIpModel(Base):
    __tablename__ = 'userip'
    username = Column(String, primary_key=True, unique=True)
    userip = Column(String)

