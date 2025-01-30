from fastapi import status
from Todos.test.utils import client,TestsessionLocal,test_todo,test_user
from Todos.router.auth import bcrypt_context
from Todos.models import Users

def test_authenticate_user(test_user):
    pass