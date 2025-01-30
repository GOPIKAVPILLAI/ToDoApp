
from fastapi import status
from Todos.test.utils import client,TestsessionLocal,test_todo,test_user
from Todos.router.auth import bcrypt_context
from Todos.models import Users


def test_admin_list_todo(test_todo):
    response=client.get('/admin/todos')
    assert response.status_code==status.HTTP_200_OK
    assert response.json()==[{
        'id':1,
        'title':"Learn coding",
        'description':"learn coding everyday",
        'priority':5,
        'complete':False,
        'owner':1
        }]
    
def test_admin_get_todo(test_todo):
    response=client.get('/admin/todo/1')
    assert response.status_code==status.HTTP_200_OK
    assert response.json()=={
        'id':1,
        'title':"Learn coding",
        'description':"learn coding everyday",
        'priority':5,
        'complete':False,
        'owner':1
        }

def test_admin_list_user(test_user):
    response=client.get('/admin/users')
    assert response.status_code==status.HTTP_200_OK
    db=TestsessionLocal()
    model=db.query(Users).filter(Users.id==1).first()
    assert bcrypt_context.verify("Test123",model.hashed_password)==True
    
    hashed_password=model.hashed_password
    assert response.json()==[{
        'id':1,
        'email':"testuser@gmail.com",
        'first_name':"user1",
        'last_name':"test",
        'role':"user",
        'hashed_password':hashed_password,
        'is_active':True
        }]
    
def test_admin_delete_user(test_user):
    response=client.delete('/admin/delete/1')
    assert response.status_code==204
    db=TestsessionLocal()
    model=db.query(Users).all()
    assert model==[]