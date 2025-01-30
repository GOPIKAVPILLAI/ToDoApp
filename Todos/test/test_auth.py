from fastapi import status
from Todos.test.utils import client,TestsessionLocal,test_todo,test_user
from Todos.router.auth import authenticate,create_access_token,ALGORITHM,SECRET_KEY,current_user
from datetime import timedelta
from jose import jwt
import pytest
from fastapi import HTTPException

def test_authenticate_user(test_user):
    db=TestsessionLocal()
    user=authenticate("testuser@gmail.com","Test123",db)
    assert user is not None
    assert user.email==test_user.email
    assert user.first_name==test_user.first_name
    
def test_not_authenticate_user(test_user):
    db=TestsessionLocal()
    user=authenticate("wronguser@gmail.com","Test123",db)
    assert user ==False
  
def test_wrong_password_authenticate_user(test_user):
    db=TestsessionLocal()
    user=authenticate("testuser@gmail.com","wrong123",db)
    assert user ==False
  
def test_create_access_token():
    email="test@test.com"
    user_id=1
    expires_delta=timedelta(days=1)
    role="user"
    token=create_access_token(email,user_id,expires_delta,role)
    decode_token=jwt.decode(token,SECRET_KEY,ALGORITHM)
    assert decode_token.get('sub')==email
    assert decode_token['id']==user_id
    assert decode_token['role']==role

@pytest.mark.asyncio 
async def test_current_user():
    encode={'sub':'test@test.com','id':1,'role':'user'}
    token=jwt.encode(encode,SECRET_KEY,ALGORITHM)
    user=await current_user(token=token)
    assert user['email']=='test@test.com'
    assert user['user_id']==1
    assert user['role']=='user'
    
    
@pytest.mark.asyncio
async def test_missing_payload_token():
    encode={'role':'user'}
    token=jwt.encode(encode,SECRET_KEY,ALGORITHM)
    with pytest.raises(HTTPException) as excp:
        await current_user(token=token)
    assert excp.value.status_code==401
    assert excp.value.detail=='Unautherized'