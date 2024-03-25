from fastapi import FastAPI, HTTPException, Depends
from typing import Optional, List, Dict
from pydantic import BaseModel
from uuid import UUID, uuid4
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",
    "localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MODEL - usually put in a seperate file
class TodoItem(BaseModel):
    id: UUID
    title: str
    completed: bool = False

class UpdateTodo(BaseModel):
    id: Optional[UUID] = None
    title: Optional[str] = None
    completed: Optional[bool] = None
    
# EMPTY STRING
todos = {}

# To do methods
# - fetch all todos
@app.get('/todos')
def get_all_todos():
    print(todos)
    return list(todos.values())


# - fetch by id
@app.get('/todos/{id}')
def get_todo(id: UUID):
    if id not in todos:
        return {"error":"title not found"}
    return todos[id]

# - post new todo
@app.post('/todos/new')
def post_todo(todo: TodoItem) -> dict:
    todos[todo.id] = todo
    return {
        "data": { "Todo added." }
    }

# - updates todo
@app.put("/todos/edit/{id}")
async def update_todo(id: UUID, todo: UpdateTodo):
    if id not in todos:
        return {'error':'ID not found'}

    if todo.title != None:
        todos[id].title = todo.title
    if todo.completed != None:
        todos[id].completed = todo.completed
    
    return todos[id]

# - removes an existing todo
@app.delete("/todos/delete/{id}")
async def delete_todo(id: UUID):
    if id not in todos:
        return {"error":"ID not found"}
    del todos[id]
    return {"msg":"todo has been deleted successfully"}