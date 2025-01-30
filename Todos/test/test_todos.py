
from fastapi import status
from Todos.test.utils import client,TestsessionLocal,test_todo
from Todos.models import ToDos



def test_list_todo(test_todo):
    response=client.get('/todos')
    assert response.status_code==status.HTTP_200_OK
    assert response.json()==[{
        'id':1,
        'title':"Learn coding",
        'description':"learn coding everyday",
        'priority':5,
        'complete':False,
        'owner':1
        }]
    
def test_get_todo(test_todo):
    response=client.get('/todo/1')
    assert response.status_code==status.HTTP_200_OK
    assert response.json()=={
        'id':1,
        'title':"Learn coding",
        'description':"learn coding everyday",
        'priority':5,
        'complete':False,
        'owner':1
        }
    
def test_get_todo_invalid(test_todo):
    response=client.get('/todo/2')
    assert response.status_code==status.HTTP_404_NOT_FOUND
    assert response.json()=={'detail':"ToDo not found"}
    
    
def test_create_todo(test_todo):
    request_data={
        'title':"New Learn coding",
        'description':"New learn coding everyday",
        'priority':5,
        'complete':False,
    }
    response=client.post('/todos',json=request_data)
    assert response.status_code==201
    db=TestsessionLocal()
    model=db.query(ToDos).filter(ToDos.id==2).first()
    assert model.title=="New Learn coding"
    assert model.description=="New learn coding everyday"
    assert model.priority==5
    assert model.complete==False
    assert model.owner==1
    
def test_update_todo(test_todo):
    request_data={
        'title':"Updated Learn coding",
        'description':"Updated learn coding everyday",
        'priority':5,
        'complete':False,
    }
    response=client.put('/todo/1',json=request_data)
    assert response.status_code==204
    db=TestsessionLocal()
    model=db.query(ToDos).filter(ToDos.id==1).first()
    assert model.title=="Updated Learn coding"
    assert model.description=="Updated learn coding everyday"
    assert model.priority==5
    assert model.complete==False
    assert model.owner==1

def test_update_todo_invalid(test_todo):
    request_data={
        'title':"Updated Learn coding",
        'description':"Updated learn coding everyday",
        'priority':5,
        'complete':False,
    }
    response=client.put('/todo/999',json=request_data)
    assert response.status_code==404
    assert response.json()=={'detail':"ToDo not found"}
     
def test_delete_todo(test_todo):
    response=client.delete('/todo/1')
    assert response.status_code==204
    db=TestsessionLocal()
    model=db.query(ToDos).all()
    assert model==[]
    
    
def test_delete_todo_invalid(test_todo):
    response=client.delete('/todo/999')
    assert response.status_code==404
    assert response.json()== {'detail': 'Todos not found'}