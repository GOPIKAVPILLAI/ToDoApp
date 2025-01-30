from Todos.database import get_db
from Todos.router.auth import current_user
from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from Todos.database import Base
from Todos.main import app
from fastapi.testclient import TestClient
from Todos.models import ToDos,Users
import pytest
from Todos.router.auth import bcrypt_context


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
        
        
        
@pytest.fixture
def test_user():
    user=Users(
        email="testuser@gmail.com",
        first_name="user1",
        last_name="test",
        role="user",
        hashed_password=bcrypt_context.hash("Test123"),
        is_active=True
    )
    db=TestsessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()