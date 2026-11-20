from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas


def get_tasks(db: Session, skip: int = 0, limit: int = 100, done: bool | None = None):
    stmt = select(models.Task).order_by(models.Task.id)
    if done is not None:
        stmt = stmt.where(models.Task.done == done)
    return list(db.scalars(stmt.offset(skip).limit(limit)))


def get_task(db: Session, task_id: int):
    return db.get(models.Task, task_id)


def create_task(db: Session, data: schemas.TaskCreate):
    task = models.Task(**data.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, task: models.Task, data: schemas.TaskUpdate):
    for field, value in data.model_dump(exclude_unset=True).items():
        # title и done не могут быть null
        if value is None and field in ("title", "done"):
            continue
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: models.Task):
    db.delete(task)
    db.commit()
