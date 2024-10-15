from fastapi import FastAPI, HTTPException, Depends
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

    def add(self, todo: TodoItem):
        todo.id = self.counter
        self.todos.append(todo)
        self.counter += 1
        return todo

    def get_all(self):
        return self.todos

    def get(self, todo_id: int):
        return next((todo for todo in self.todos if todo.id == todo_id), None)

    def update(self, todo_id: int, updated_todo: TodoItem):
        for i, todo in enumerate(self.todos):
            if todo.id == todo_id:
                updated_todo.id = todo_id
                self.todos[i] = updated_todo
                return updated_todo
        return None

    def delete(self, todo_id: int):
        for i, todo in enumerate(self.todos):
            if todo.id == todo_id:
                return self.todos.pop(i)
        return None

# Service
class TodoService:
    def __init__(self, model: TodoModel):
        self.model = model

    def create_todo(self, todo: TodoItem):
        return self.model.add(todo)

    def get_todos(self):
        return self.model.get_all()

    def get_todo(self, todo_id: int):
        todo = self.model.get(todo_id)
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        return todo

    def update_todo(self, todo_id: int, todo: TodoItem):
        updated_todo = self.model.update(todo_id, todo)
        if updated_todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        return updated_todo

    def delete_todo(self, todo_id: int):
        deleted_todo = self.model.delete(todo_id)
        if deleted_todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        return deleted_todo

# Dependency Injection
def get_todo_service():
    model = TodoModel()
    return TodoService(model)

# Controller
@app.post("/todos", response_model=TodoItem)
async def create_todo(todo: TodoItem, service: TodoService = Depends(get_todo_service)):
    return service.create_todo(todo)

@app.get("/todos", response_model=List[TodoItem])
async def read_todos(service: TodoService = Depends(get_todo_service)):
    return service.get_todos()

@app.get("/todos/{todo_id}", response_model=TodoItem)
async def read_todo(todo_id: int, service: TodoService = Depends(get_todo_service)):
    return service.get_todo(todo_id)

@app.put("/todos/{todo_id}", response_model=TodoItem)
async def update_todo(todo_id: int, todo: TodoItem, service: TodoService = Depends(get_todo_service)):
    return service.update_todo(todo_id, todo)

@app.delete("/todos/{todo_id}", response_model=TodoItem)
async def delete_todo(todo_id: int, service: TodoService = Depends(get_todo_service)):
    return service.delete_todo(todo_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)