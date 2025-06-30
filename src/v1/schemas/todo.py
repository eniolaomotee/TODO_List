import uuid

from pydantic import BaseModel, Field,  ConfigDict
from typing import List


class TodoCreate(BaseModel):
    title: str = Field(description="Title of the todo item")
    description: str | None = Field(None, description="Description of the todo item")


class TodoUpdate(BaseModel):
    title: str | None = Field(description="Title of the todo item")
    description: str | None = Field(description="Description of the todo item")


class TodoOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    todo_uid: uuid.UUID
    title: str
    description: str


class PaginatedTodoResponse(BaseModel):
    data: List[TodoOutput]
    page: int
    limit: int
    total: int