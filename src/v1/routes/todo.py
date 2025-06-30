from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.dependencies import AccessTokenBearer
from src.db.db import get_session
from src.v1.schemas.todo import TodoCreate, TodoOutput, TodoUpdate, PaginatedTodoResponse
from src.v1.service.todo import TodoService
import logging

logger = logging.getLogger(__name__)

todo_router = APIRouter()

todo_service = TodoService()
access_bearer_token = AccessTokenBearer()




@todo_router.post("/", response_model=TodoOutput, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo_data: TodoCreate,
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_bearer_token),
):
    """
    Create a new todo item.
    """
    user_uid = token_details.get("user")["uid"]
    logger.debug("THis is user_uid %s", user_uid)
    todo = await todo_service.create_todo(todo_data=todo_data, user_uid=user_uid, session=session)
    return todo

@todo_router.get("/", response_model=PaginatedTodoResponse)
async def get_todo(
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_bearer_token),
    page: int = Query(1, ge=1),
    limit: int = Query(10,ge=1,le=100)
):
    """
    Get a logged in user todo.
    """
    user_uid = token_details.get("user")["uid"]
    logger.debug("User Uid is %s", user_uid)
    todo = await todo_service.get_todo(user_uid=user_uid, session=session, page=page, limit=limit)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )

    return todo


@todo_router.get("/search", response_model=list[TodoCreate])
async def search_todos(
    search_term: str = Query(min_length=1, max_length=100, description="Search keyword in title or description"),
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_bearer_token),
):
    """
    Search for todo items by title and/or completion status.
    """
    todos = await todo_service.search_todos(search_term=search_term, session=session)

    return todos

@todo_router.get("/count")
async def count_todos(session: AsyncSession = Depends(get_session), token_details=Depends(access_bearer_token)):
    to_dos = await todo_service.count_todos(session=session)
    
    return to_dos


@todo_router.get("/{todo_uid}", response_model=TodoOutput)
async def get_todo_by_id(
    todo_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_bearer_token),
):
    """
    Get a todo item by its ID.
    """
    todo = await todo_service.get_todo_by_uid(todo_uid=todo_uid, session=session)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )

    return todo


@todo_router.put("/{todo_uid}", response_model=TodoOutput)
async def update_todo(
    todo_uid: str,
    todo_data: TodoUpdate,
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_bearer_token),
):
    """
    Update an existing todo item.
    """
    todo = await todo_service.update_todo(
        todo_uid=todo_uid, todo_data=todo_data, session=session
    )

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )

    return todo


@todo_router.delete("/{todo_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_bearer_token),
):
    """
    Delete a todo item by its ID.
    """
    await todo_service.delete_todo(todo_uid=todo_uid, session=session)

    return {"detail": "Todo deleted successfully"}






# @todo_router.get("/count")
# async def count_todos(
#     session: AsyncSession = Depends(get_session),
#     token_details=Depends(access_bearer_token),
# ):
#     todos = await todo_service.count_todos(session=session)
#     return todos


# 2c0f4216-09bc-49ae-b527-e7e8e484c8ed