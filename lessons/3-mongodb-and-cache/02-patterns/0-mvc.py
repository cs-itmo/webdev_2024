from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Model
class TodoItem(BaseModel):
    id: Optional[int] = None
    task: str
    completed: bool = False

class TodoModel:
    def __init__(self):
        self.todos = []
        self.counter = 1

    def add_todo(self, todo: TodoItem):
        todo.id = self.counter
        self.todos.append(todo)
        self.counter += 1
        return todo

    def get_todos(self):
        return self.todos

    def get_todo(self, todo_id: int):
        for todo in self.todos:
            if todo.id == todo_id:
                return todo
        return None

    def update_todo(self, todo_id: int, updated_todo: TodoItem):
        for i, todo in enumerate(self.todos):
            if todo.id == todo_id:
                updated_todo.id = todo_id
                self.todos[i] = updated_todo
                return updated_todo
        return None

    def delete_todo(self, todo_id: int):
        for i, todo in enumerate(self.todos):
            if todo.id == todo_id:
                return self.todos.pop(i)
        return None

# Controller
todo_model = TodoModel()

@app.post("/todos", response_model=TodoItem)
async def create_todo(todo: TodoItem):
    return todo_model.add_todo(todo)

@app.get("/todos", response_model=List[TodoItem])
async def read_todos():
    return todo_model.get_todos()

@app.get("/todos/{todo_id}", response_model=TodoItem)
async def read_todo(todo_id: int):
    todo = todo_model.get_todo(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.put("/todos/{todo_id}", response_model=TodoItem)
async def update_todo(todo_id: int, todo: TodoItem):
    updated_todo = todo_model.update_todo(todo_id, todo)
    if updated_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated_todo

@app.delete("/todos/{todo_id}", response_model=TodoItem)
async def delete_todo(todo_id: int):
    deleted_todo = todo_model.delete_todo(todo_id)
    if deleted_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return deleted_todo

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)