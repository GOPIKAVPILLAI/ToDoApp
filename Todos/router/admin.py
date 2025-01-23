from typing import Annotated
from fastapi import HTTPException,Path,APIRouter,Depends
from pydantic import BaseModel, Field
from Todos.models import ToDos,Users
from starlette import status
from Todos.database import db_dependency
from Todos.router.auth import current_user

user_dependency=Annotated[dict,Depends(current_user)]
router=APIRouter(
    prefix="/admin",
    tags=['admin']
)

@router.get("/todos",status_code=status.HTTP_200_OK)
async def list_todo(user:user_dependency,db:db_dependency):
    if user is None or user.get("role")!="admin":
        raise HTTPException(status_code=401,detail="Autentication Failed")
    return db.query(ToDos).all()


@router.get("/todo/{todo_id}",status_code=status.HTTP_200_OK)
async def get_todo(user:user_dependency,db:db_dependency,todo_id:int=Path(gt=0)):
    if user is None or user.get("role")!="admin":
        raise HTTPException(status_code=401,detail="Autentication Failed")
    return db.query(ToDos).filter(ToDos.id==todo_id).first()


    
@router.delete("/delete/{user_id}")
async def delete_user(user:user_dependency,db:db_dependency,user_id:int=Path(gt=0)):
    if user is None or user.get("role")!="admin":
        raise HTTPException(status_code=401,detail="Autentication Failed")
    user_data=db.query(Users).filter(Users.id==user_id).first()
    if user_data is None:
        raise HTTPException(status_code=404,detail="user not found")
    db.query(Users).filter(Users.id==user_id).delete()
    db.commit()
    
    

#list all users in db
@router.get("/users",status_code=status.HTTP_200_OK) 
async def list_users(user:user_dependency,db:db_dependency):
    if user is None or user.get("role")!="admin":
        raise HTTPException(status_code=401,detail="Autentication Failed")
    return db.query(Users).all()