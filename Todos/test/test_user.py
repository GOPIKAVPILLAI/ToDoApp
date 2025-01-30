from fastapi import status
from Todos.test.utils import client,TestsessionLocal,test_todo,test_user
from Todos.models import Users
from Todos.router.auth import bcrypt_context

def test_change_password(test_user):
    data={
    'password' : "Test123",
    'new_password' : "NewTest123",
    'confirm_password': "NewTest123"
    }
    response=client.patch('/user/change-password',json=data)
    assert response.json()=={"message":"password Changed Successfully"}
    db=TestsessionLocal()
    model=db.query(Users).filter(Users.id==1).first()
    assert bcrypt_context.verify("NewTest123",model.hashed_password)==True
    
    
def test_change_new_password_confirm_password_not_match(test_user):
    data={
    'password' : "Test123",
    'new_password' : "NewTest123",
    'confirm_password': "Test123"
    }
    response=client.patch('/user/change-password',json=data)
    assert response.json()=={"message":"New Password Not Matching to Confirm password"}
    
    
def test_change_password_password_not_match(test_user):
    data={
    'password' : "NotInDBTest123",
    'new_password' : "NewTest123",
    'confirm_password': "NewTest123"
    }
    response=client.patch('/user/change-password',json=data)
    assert response.json()=={"message":"Password Not Matching to password in db"}