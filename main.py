import fastapi
import databases
import sqlalchemy
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import asyncio

app = fastapi.FastAPI()

# Database configuration
DATABASE_URL = "sqlite:///todo.db"
database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(DATABASE_URL)

# Define the data model
class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    category: Optional[str] = None
    deadline: Optional[datetime] = None

# Create the database tables
async def create_tables():
    await database.connect()
    await engine.execute(sqlalchemy.schema.CreateTable(Task.__table__))
    await database.disconnect()

# Get all tasks
@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    await create_tables()
    query = Task.__table__.select()
    return await database.fetch_all(query)

# Create a new task
@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    await create_tables()
    query = Task.__table__.insert().values(task.dict())
    last_record_id = await database.execute(query)
    return await database.fetch_one(Task.__table__.select().where(Task.id == last_record_id))

# Get a task by ID
@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    await create_tables()
    query = Task.__table__.select().where(Task.id == task_id)
    task = await database.fetch_one(query)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Update a task by ID
@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    await create_tables()
    query = Task.__table__.update().where(Task.id == task_id).values(task.dict())
    await database.execute(query)
    return await get_task(task_id)

# Delete a task by ID
@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    await create_tables()
    query = Task.__table__.delete().where(Task.id == task_id)
    await database.execute(query)

# Define the async function
async def my_async_function():
    task = asyncio.create_task(my_async_function())
    
# Wait for the task to complete
await task
