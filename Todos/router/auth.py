from datetime import datetime, timedelta
from fastapi import APIRouter,Depends, HTTPException,Path
from fastapi import APIRouter,Depends, HTTPException,Path
from starlette import status
from pydantic import BaseModel
from Todos.models import Users
from Todos.database import db_dependency
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from typing import Annotated
from jose import jwt,JWTError

SECRET_KEY='98a5f275b7e2997a0b80f36c56f42200'
ALGORITHM='HS256'
EXP_TIME=timedelta(minutes=20)
bcrypt_context=CryptContext (schemes=['bcrypt'],deprecated='auto')
oauth2_bearer=OAuth2PasswordBearer(tokenUrl='auth/token')

router=APIRouter(
    prefix='/auth',
    tags=['auth']
)

class Token(BaseModel):
    access_token : str
    refresh_token : str
    token_type : str
    
class RefreshRequest(BaseModel):
    refresh_token:str
       
class loginUserRequest(BaseModel):
    email:str
    password:str
    
class CreateUserRequest(BaseModel):
    email : str
    first_name : str
    last_name : str
    password : str
    role : str
 
""" check the user is authenticated or not,
    if the users email and password match to the email and password 
    in our db then return the user   """
def authenticate(email,password,db):
    user=db.query(Users).filter(Users.email==email).first()  
    if not user:
        return False
    if not bcrypt_context.verify(password,user.hashed_password):
        return False
    return user
    
    
"""create JWT access token and return token
"""
def create_access_token(email:str,user_id:int,expires_delta:timedelta,role:str):
    expires=datetime.utcnow()+expires_delta
    encode={"sub":email,"id":user_id,"exp":expires,"role":role}
    
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)



@router.get("/users",status_code=status.HTTP_200_OK) 
async def list_users(token:Annotated[str,Depends(oauth2_bearer)],db:db_dependency):
    return db.query(Users).all()
    
#user registration
@router.post("/register",status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency,request:CreateUserRequest):
    user_model=Users(
        email=request.email,
        first_name=request.first_name,
        last_name=request.last_name,
        hashed_password=bcrypt_context.hash(request.password),
        role=request.role,
        is_active=True
        
    )
    db.add(user_model)
    db.commit()
    
#login with email and password to get jwt access token
@router.post("/token",response_model=Token,status_code=status.HTTP_201_CREATED)
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends(loginUserRequest)],db:db_dependency):
    user=authenticate(form_data.email,form_data.password,db)
    if not user:
         raise HTTPException(status_code=401,detail="Unautherized")
    token=create_access_token(user.email,user.id,timedelta(minutes=20),user.role)
    return {"access":token,"token_type":"beaer"}


#this function return the current logined users email and user id
async def current_user(token:Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        email=payload.get('sub')
        id=payload.get('id')
        role=payload.get('role')
        if email is None or id is None:
            raise HTTPException(status_code=401,detail="Unautherized")
        return {"user_id":id,"email":email,"role":role}
    except JWTError:
        raise HTTPException(status_code=401,detail="Unautherized")