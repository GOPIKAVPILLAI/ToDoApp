from typing import Annotated
from fastapi import HTTPException,Path,APIRouter,Depends
from pydantic import BaseModel, Field
from Todos.models import ToDos,Users
from starlette import status
from Todos.database import db_dependency
from Todos.router.auth import current_user,bcrypt_context


class PasswordRequest(BaseModel):
    password : str
    new_password : str
    confirm_password: str
    
    
user_dependency=Annotated[dict,Depends(current_user)]
router=APIRouter(
    prefix="/user",
    tags=['user']
)

#get the profile details of current logined user
@router.get("/profile",status_code=status.HTTP_200_OK)
async def get_user_profile(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail="Authentication Failed")
    return db.query(Users).filter(Users.id==user.get('user_id')).first()

#change password of current logined user
@router.patch("/change-password",response_model=dict)
async def change_user_password(user:user_dependency,db:db_dependency,request:PasswordRequest):
    if request.new_password !=request.confirm_password:
        return {"message":"New Password Not Matching to Confirm password"}
    
    if user is None:
        raise HTTPException(status_code=401,detail="Authentication Failed")
    user_data=db.query(Users).filter(Users.id==user.get('user_id')).first()
    if not bcrypt_context.verify(request.password,user_data.hashed_password):
        return  {"message":"Password Not Matching to password in db"}
    user_data.hashed_password=bcrypt_context.hash(request.new_password)
    db.add(user_data)
    db.commit()
    return {"message":"password Changed Successfully"}
    