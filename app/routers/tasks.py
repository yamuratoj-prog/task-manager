from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])


def _get_or_404(db: Session, task_id: int):
    task = crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")
    return task


@router.get("", response_model=list[schemas.TaskRead])
def list_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    done: bool | None = Query(None, description="Фильтр: выполненные / невыполненные"),
    db: Session = Depends(get_db),
):
    return crud.get_tasks(db, skip=skip, limit=limit, done=done)


@router.post("", response_model=schemas.TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(data: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, data)


@router.get("/{task_id}", response_model=schemas.TaskRead)
def read_task(task_id: int, db: Session = Depends(get_db)):
    return _get_or_404(db, task_id)


@router.patch("/{task_id}", response_model=schemas.TaskRead)
def update_task(task_id: int, data: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = _get_or_404(db, task_id)
    return crud.update_task(db, task, data)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = _get_or_404(db, task_id)
    crud.delete_task(db, task)
