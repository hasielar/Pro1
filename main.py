from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Task(BaseModel):
    id: int
    title: str
    completed: bool

tasks = []

@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    return tasks

@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    tasks.append(task)
    return task

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, updated_task: Task):
    task_index = next((index for index, t in enumerate(tasks) if t.id == task_id), None)
    if task_index is None:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks[task_index] = updated_task
    return updated_task

@app.delete("/tasks/{task_id}", response_model=Task)
async def delete_task(task_id: int):
    task = next((t for t in tasks if t.id == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks.remove(task)
    return task
