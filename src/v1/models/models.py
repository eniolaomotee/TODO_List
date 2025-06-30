import uuid
from datetime import datetime
from typing import List, Optional

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, Relationship, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"
    """
    Represents a user in the system.
    """
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID, primary_key=True, unique=True, nullable=False, default=uuid.uuid4
        )
    )
    email: str
    hashed_password: str
    is_active: bool = False
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    
    todo: List["TodoItem"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy":"selectin"})
    
    

    def repr__(self):
        return f"User(uid={self.uid}, email={self.email}, is_active={self.is_active})"


class TodoItem(SQLModel, table=True):
    __tablename__ = "todo_items"

    """     Represents a todo item in the system """
    todo_uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID, primary_key=True, unique=True, nullable=False, default=uuid.uuid4
        )
    )
    title: str
    description: Optional[str]
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    
    user : Optional[User] = Relationship(back_populates="todo")


    def repr__(self):
        return f"TodoItem(todo_uid={self.todo_uid}, title={self.title}, is_completed={self.is_completed})"
