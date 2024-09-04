from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()
todo_store = {}

class TodoItem(BaseModel):
    id: int
    title: str = Field(max_length=100)
    description: Optional[str] = None
    completed: bool = False

class CreateTodoItem(BaseModel):
    title: str = Field(max_length=100)
    description: Optional[str] = None
    completed: bool = False

@app.post("/todos/", response_model=TodoItem)
async def create_todo_item(todo: CreateTodoItem):
    new_id = max(todo_store.keys(), default=0) + 1
    if new_id in todo_store:
        raise HTTPException(status_code=400, detail="Todo item with this ID already exists")
    
    new_todo = TodoItem(id=new_id, **todo.model_dump())
    todo_store[new_id] = new_todo
    return new_todo

@app.get("/todos/", response_model=List[TodoItem])
async def get_todo_items():
    return list(todo_store.values())

@app.get("/todos/{todo_id}", response_model=TodoItem)
async def get_todo_item(todo_id: int):
    if todo_id not in todo_store:
        raise HTTPException(status_code=404, detail="Todo item not found")
    return todo_store[todo_id]

@app.put("/todos/{todo_id}", response_model=TodoItem)
async def update_todo_item(todo_id: int, todo: TodoItem):
    if todo_id not in todo_store:
        raise HTTPException(status_code=404, detail="Todo item not found")
    todo_store[todo_id] = todo
    return todo

@app.delete("/todos/{todo_id}", response_model=TodoItem)
async def delete_todo_item(todo_id: int):
    if todo_id not in todo_store:
        raise HTTPException(status_code=404, detail="Todo item not found")
    deleted_todo = todo_store.pop(todo_id)
    return deleted_todo

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
