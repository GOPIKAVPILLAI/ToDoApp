from typing import Annotated
from fastapi import HTTPException,Path,APIRouter,Depends
from pydantic import BaseModel, Field
from Todos.models import ToDos
from starlette import status
from Todos.database import db_dependency
from Todos.router.auth import current_user

user_dependency=Annotated[dict,Depends(current_user)]
router=APIRouter(
    tags=['todo']
)



        
        
class ToDoRequest(BaseModel):
    title :str =Field(min_length=3)
    description : str =Field(min_length=3,max_length=100)
    priority : int = Field(gt=0,lt=6)
    complete : bool 
    





"""List all the ToDo of a perticular logined user
"""
@router.get("/todos",status_code=status.HTTP_200_OK)
async def list_todos(user:user_dependency,db:db_dependency):
    return db.query(ToDos).filter(ToDos.owner==user.get("user_id")).all()
    
    
    
""" only retrive todo from table with todo_id if the logined user is owner of that todo
"""
@router.get("/todo/{todo_id}",status_code=status.HTTP_200_OK)
async def get_todo(user:user_dependency,db:db_dependency,todo_id:int=Path(gt=0)):

    data= db.query(ToDos).filter(ToDos.owner==user.get("user_id"),ToDos.id==todo_id).first()
    if data:
        return data
    raise HTTPException(status_code=404,detail="ToDo not found")
 
 
 
# Create ToDo   
@router.post("/todos",status_code=status.HTTP_201_CREATED)
async def create_todos(user:user_dependency,db:db_dependency,todo_request:ToDoRequest):
    if not user:
        raise HTTPException(status_code=401,detail="Autherization Failed")
    print(user)
    todo_model=ToDos(**todo_request.dict(),owner=user.get('user_id'))
    db.add(todo_model)
    db.commit()



#update Todo   
@router.put("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_todos(user:user_dependency,db:db_dependency,todo_request:ToDoRequest,todo_id:int=Path(gt=0)):
    
    todo_model=db.query(ToDos).filter(ToDos.owner==user.get("user_id"),ToDos.id==todo_id).first()
    
    if todo_model is None:
        raise HTTPException(status_code=404,detail="ToDo not found")
    
    todo_model.title=todo_request.title
    todo_model.description=todo_request.description
    todo_model.priority=todo_request.priority
    todo_model.complete=todo_request.complete
    
    db.add(todo_model)
    db.commit()
    
    
#delete todo
@router.delete("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user:user_dependency,db:db_dependency,todo_id:int=Path(gt=0)):
    
    todo_model=db.query(ToDos).filter(ToDos.owner==user.get("user_id"),ToDos.id==todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404,detail="Todos not found")
    todo_model=db.query(ToDos).filter(ToDos.id==todo_id).delete()
    db.commit()
    
    
#This is the router to change the status of ToDo complete,if call the router the given todo complete status changed to true ,that means task completed successfully
@router.put("/complete/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def todo_completed(user:user_dependency,db:db_dependency,todo_id:int=Path(gt=0)):
    
    todo_model=db.query(ToDos).filter(ToDos.owner==user.get("user_id"),ToDos.id==todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404,detail="Todo Not Found")
    todo_model.complete=True
    db.add(todo_model)
    db.commit()