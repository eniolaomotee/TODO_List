from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.db import get_session
from src.v1.schemas.todo import TodoCreate, TodoUpdate
from src.v1.service.todo import TodoService
from typing import List

todo_router = APIRouter()

todo_service = TodoService()


@todo_router.post("/", response_model=TodoCreate, status_code=status.HTTP_201_CREATED)
async def create_todo(todo_data: TodoCreate, session:AsyncSession = Depends(get_session)):
    """
    Create a new todo item.
    """
    todo = await todo_service.create_todo(todo_data=todo_data, session=session)
    return todo

@todo_router.get("/{todo_uid}", response_model=TodoCreate)
async def get_todo(todo_uid: int, session: AsyncSession = Depends(get_session)):
    """
    Get a todo item by its ID.
    """
    todo = await todo_service.get_todo_by_id(todo_uid=todo_uid, session=session)
    
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    
    return todo

@todo_router.put("/{todo_uid}", response_model=TodoUpdate)
async def update_todo(todo_uid: int, todo_data: TodoUpdate, session: AsyncSession = Depends(get_session)):
    """
    Update an existing todo item.
    """
    todo = await todo_service.update_todo(todo_uid=todo_uid, todo_data=todo_data, session=session)
    
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    
    return todo

@todo_router.delete("/{todo_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_uid: int, session: AsyncSession = Depends(get_session)):
    """
    Delete a todo item by its ID.
    """
    await todo_service.delete_todo(todo_id=todo_uid, session=session)
    
    return {"detail": "Todo deleted successfully"}

@todo_router.get("/", response_model=List[TodoCreate])
async def list_todos(session: AsyncSession = Depends(get_session)):
    """
    List all todo items.
    """
    todos = await todo_service.get_all_todos(session=session)
    
    return todos

@todo_router.get("/search", response_model=list[TodoCreate])
async def search_todos(title: str | None = None, completed: bool | None = None, session: AsyncSession = Depends(get_session)):
    """
    Search for todo items by title and/or completion status.
    """
    todos = await todo_service.search_todos(title=title, completed=completed, session=session)
    
    return todos

@todo_router.get("/count", response_model=int)
async def count_todos(session: AsyncSession = Depends(get_session)):
   
   todos = await todo_service.count_todos(session=session)
   return todos
