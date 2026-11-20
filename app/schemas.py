from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=200, examples=["Купить молоко"])
    description: str | None = Field(default=None, examples=["2 литра, 3.2%"])


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    """Все поля необязательны — можно менять только то, что нужно (PATCH)."""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    done: bool | None = None


class TaskRead(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    done: bool
    created_at: datetime
