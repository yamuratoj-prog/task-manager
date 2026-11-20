from contextlib import asynccontextmanager

from fastapi import FastAPI

from . import models  # noqa: F401  (нужно, чтобы модели зарегистрировались до create_all)
from .database import Base, engine
from .routers import tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    # При старте создаём таблицы, если их ещё нет
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Task Manager API",
    description="Простой REST API для управления задачами (FastAPI + SQLite).",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(tasks.router)


@app.get("/", tags=["service"])
def root():
    return {"message": "Task Manager API работает", "docs": "/docs"}


@app.get("/health", tags=["service"])
def health():
    return {"status": "ok"}
