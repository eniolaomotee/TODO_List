import uuid

from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    title: str = Field(description="Title of the todo item")
    description: str | None = Field(None, description="Description of the todo item")


class TodoUpdate(BaseModel):
    title: str | None = Field(description="Title of the todo item")
    description: str | None = Field(description="Description of the todo item")


class TodoOutput(BaseModel):
    todo_uid: uuid.UUID
    title: str
    description: str
