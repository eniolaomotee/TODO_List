from src.v1.models.models import TodoItem
from sqlmodel import select, desc
from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.v1.schemas.todo import TodoCreate, TodoUpdate


class TodoService:
    async def get_todo_by_id(self, todo_id: int, session: AsyncSession):
        "Get a todo item by its ID."
        statement = select(TodoItem).where(TodoItem.todo_uid == todo_id)
        result = await session.exec(statement)
        todo = result.first()
        return todo

    async def create_todo(self, todo_data: TodoCreate, session: AsyncSession):
        "Create a new todo item."
        new_todo = TodoItem(**todo_data.model_dump())
        session.add(new_todo)
        await session.commit()
        await session.refresh(new_todo)
        return new_todo

    async def update_todo(self, todo_id: int, todo_data: TodoUpdate, session: AsyncSession):
        "Update an existing todo item."
        todo = await self.get_todo_by_id(todo_id=todo_id, session=session)
        
        if not todo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
        
        for key, value in todo_data.model_dump().items():
            setattr(todo, key, value)
        
        session.add(todo)
        await session.commit()
        await session.refresh(todo)
        
        return todo

    async def delete_todo(self, todo_id: int, session: AsyncSession):
        "Delete a todo item by its ID."
        todo = await self.get_todo_by_id(todo_id=todo_id, session=session)
        
        if not todo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
        
        await session.delete(todo)
        await session.commit()
        
    async def get_all_todos(self,session: AsyncSession):
        "Get all todo items."        
        statement = select(TodoItem).order_by(TodoItem.created_at.desc())
        result = await session.exec(statement)
        todos = result.all()
        return todos
    
    async def search_todos(self, search_term: str, session: AsyncSession):
        "Search for todo items by title or description."
        statement = select(TodoItem).where(
            (TodoItem.title.ilike(f"%{search_term}%")) |
            (TodoItem.description.ilike(f"%{search_term}%"))
        ).order_by(TodoItem.created_at.desc())
        
        result = await session.exec(statement)
        todos = result.all()
        
        return todos
    
    async def count_todos(self, session: AsyncSession):
        "Count the total number of todo items."
        statement = select(TodoItem)
        result = await session.exec(statement)
        count = result.rowcount
        return count