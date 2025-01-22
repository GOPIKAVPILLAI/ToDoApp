from Todos.database import Base
from sqlalchemy import Column,Integer,Boolean,String,ForeignKey
class Users(Base):
    
    __tablename__='users'
    id=Column(Integer,primary_key=True,index=True)
    email=Column(String,unique=True)
    first_name=Column(String,max_length=100)
    last_name=Column(String,max_length=100)
    hashed_password=Column(String)
    is_active=Column(Boolean,default=True)
    role=Column(String)
    
    
    
class ToDos(Base):

    __tablename__ = 'todos'
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    description=Column(String)
    priority=Column(Integer)
    complete=Column(Boolean,default=False)
    owner=Column(Integer,ForeignKey('users.id'))