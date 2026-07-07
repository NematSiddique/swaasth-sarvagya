from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.api.deps import SessionDep
from app.models import Hospital, Message

router = APIRouter(prefix="/hospitals", tags=["hospitals"])


@router.post("/", response_model=Hospital)
def create_hospital(*, session: SessionDep, hospital_in: Hospital) -> Any:
    """
    Create new hospital.
    """
    hospital = Hospital.model_validate(hospital_in)
    session.add(hospital)
    session.commit()
    session.refresh(hospital)
    return hospital


@router.get("/", response_model=list[Hospital])
def read_hospitals(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve hospitals.
    """
    statement = select(Hospital).offset(skip).limit(limit)
    hospitals = session.exec(statement).all()
    return hospitals


@router.get("/{hospital_id}", response_model=Hospital)
def read_hospital(*, session: SessionDep, hospital_id: int) -> Any:
    """
    Get hospital by ID.
    """
    hospital = session.get(Hospital, hospital_id)
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return hospital


@router.put("/{hospital_id}", response_model=Hospital)
def update_hospital(
    *, session: SessionDep, hospital_id: int, hospital_in: Hospital
) -> Any:
    """
    Update a hospital.
    """
    hospital = session.get(Hospital, hospital_id)
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    update_dict = hospital_in.model_dump(exclude_unset=True)
    hospital.sqlmodel_update(update_dict)
    session.add(hospital)
    session.commit()
    session.refresh(hospital)
    return hospital


@router.delete("/{hospital_id}", response_model=Message)
def delete_hospital(*, session: SessionDep, hospital_id: int) -> Message:
    hospital = session.get(Hospital, hospital_id)
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    session.delete(hospital)
    session.commit()
    return Message(message="Hospital deleted successfully")
