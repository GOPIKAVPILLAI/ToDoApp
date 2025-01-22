from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends

SQLALCHEMY_DATABASE_URL="sqlite:///./todosapp.db"

engine=create_engine(SQLALCHEMY_DATABASE_URL,connect_args={'check_same_thread':False})

sessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()

def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()
        
#here this is the database dependency injection
db_dependency=Annotated[Session,Depends(get_db)]