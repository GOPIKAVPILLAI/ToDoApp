from Todos.database import get_db
from Todos.router.auth import current_user
from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from Todos.database import Base
from Todos.main import app
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from Todos.models import ToDos

SQLALCHEMY_DATABASE_URL="sqlite:///./test.db"

engine=create_engine(SQLALCHEMY_DATABASE_URL,connect_args={'check_same_thread':False},poolclass=StaticPool)

TestsessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db=TestsessionLocal()
    try:
        yield db
    finally:
        db.close()
    
def override_get_current_user():
    return {"user_id":1,"email":"test@gmail.com","role":"admin"}

app.dependency_overrides[get_db]=override_get_db    
app.dependency_overrides[current_user]=override_get_current_user

client=TestClient(app)

@pytest.fixture
def test_todo():
    todo=ToDos(
        title="Learn coding",
        description="learn coding everyday",
        priority=5,
        complete=False,
        owner=1
    )
    db=TestsessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()

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