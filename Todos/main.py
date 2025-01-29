from fastapi import FastAPI
from Todos.router import auth,todo,admin,user
from Todos.database import engine
from Todos import models

app=FastAPI()

@app.get('/healthy')
async def health_check():
    return {"status":"Healthy"}


app.include_router(auth.router)
app.include_router(todo.router)
app.include_router(admin.router)
app.include_router(user.router)
models.Base.metadata.create_all(bind=engine)