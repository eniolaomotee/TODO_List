from fastapi import HTTPException, status
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import func
from src.v1.models.models import TodoItem
from src.v1.schemas.todo import TodoCreate, TodoUpdate
import logging
from uuid import UUID

logger = logging.getLogger(__name__)

class TodoService:
    async def get_todo_by_uid(self, todo_uid: int, session: AsyncSession):
        "Get a todo item by its ID."
        statement = select(TodoItem).where(TodoItem.todo_uid == todo_uid)
        result = await session.exec(statement)
        todo = result.first()
        return todo
    
    async def get_todo(self, user_uid: str, session: AsyncSession, page: int =1, limit :int=10):
        "Get a user todo."
        offset = (page - 1 ) * limit
        statement = select(TodoItem).where(TodoItem.user_uid == user_uid).offset(offset).limit(limit)
        result = await session.exec(statement)
        todo = result.all()
        
        
        count_statm = select(func.count()).select_from(TodoItem).where(TodoItem.user_uid == user_uid)
        total_result = await session.exec(count_statm)
        total = total_result.one()
        
        return {
            "data": todo,
            "page":page,
            "limit":limit,
            "total":total
        }
        
    async def create_todo(self, todo_data: TodoCreate, user_uid:str, session: AsyncSession):
        "Create a new todo item."
        new_todo = TodoItem(**todo_data.model_dump(), user_uid=UUID(user_uid))
        session.add(new_todo)
        await session.commit()
        await session.refresh(new_todo)
        return new_todo

    async def update_todo(
        self, todo_uid: int, todo_data: TodoUpdate, session: AsyncSession
    ):
        "Update an existing todo item."
        todo = await self.get_todo_by_uid(todo_uid=todo_uid, session=session)

        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
            )

        for key, value in todo_data.model_dump().items():
            setattr(todo, key, value)

        session.add(todo)
        await session.commit()
        await session.refresh(todo)

        return todo

    async def delete_todo(self, todo_uid: int, session: AsyncSession):
        "Delete a todo item by its ID."
        todo = await self.get_todo_by_uid(todo_uid=todo_uid, session=session)

        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
            )

        await session.delete(todo)
        await session.commit()

    async def get_all_todos(self, session: AsyncSession):
        "Get all todo items."
        statement = select(TodoItem).order_by(TodoItem.created_at.desc())
        result = await session.exec(statement)
        todos = result.all()
        return todos

    async def search_todos(self, search_term: str, session=AsyncSession,):
        "Search for todo items by title or description."
        statement = (
            select(TodoItem)
            .where(
                (TodoItem.title.ilike(f"%{search_term}%"))
                | (TodoItem.description.ilike(f"%{search_term}%"))
            )
            .order_by(TodoItem.created_at.desc())
        )

        result = await session.exec(statement)
        todos = result.all()

        return todos

    async def count_todos(self, session: AsyncSession):
        "Count the total number of todo items."
        statement = select(func.count()).select_from(TodoItem)
        result = await session.exec(statement)
        count = result.all()
        return len(count)
