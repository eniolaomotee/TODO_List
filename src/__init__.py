import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.db.db import close_db, init_db
from src.utils.logging_conf import configure_logging
from src.v1.routes.auth import auth_router
from src.v1.routes.todo import todo_router

logger = logging.getLogger(__name__)




@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan event handler for initializing and closing the database.
    This will run once when the application starts and once when it shuts down.
    """
    print("Starting application starting...")
    configure_logging()
    logger.info("Logging works!!!")
    await init_db()
    yield
    await close_db()
    print("Application shutdown complete.")


version = "v1"
version_prefix = f"/api/{version}"

app = FastAPI(
    title="TODO List API Project",
    description="A simple TODO List API built with FastAPI and SQLModel.",
    version=version,
    lifespan=lifespan,
)

app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["Auth"])
app.include_router(todo_router, prefix=f"/api/{version}/todo", tags=["Todo"])


# uvicorn src:app --reload         