from fastapi import FastAPI
from Todos.router import auth,todo
from Todos.database import engine
from Todos import models

app=FastAPI()
app.include_router(auth.router)
app.include_router(todo.router)
models.Base.metadata.create_all(bind=engine)