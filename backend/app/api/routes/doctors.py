from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.api.deps import SessionDep
from app.models import Doctor, Message

router = APIRouter(prefix="/doctors", tags=["doctors"])


@router.post("/", response_model=Doctor)
def create_doctor(*, session: SessionDep, doctor_in: Doctor) -> Any:
    """
    Create new doctor.
    """
    doctor = Doctor.model_validate(doctor_in)
    session.add(doctor)
    session.commit()
    session.refresh(doctor)
    return doctor


@router.get("/", response_model=list[Doctor])
def read_doctors(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve doctors.
    """
    statement = select(Doctor).offset(skip).limit(limit)
    doctors = session.exec(statement).all()
    return doctors


@router.get("/{doctor_id}", response_model=Doctor)
def read_doctor(*, session: SessionDep, doctor_id: int) -> Any:
    """
    Get doctor by ID.
    """
    doctor = session.get(Doctor, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


@router.put("/{doctor_id}", response_model=Doctor)
def update_doctor(*, session: SessionDep, doctor_id: int, doctor_in: Doctor) -> Any:
    """
    Update a doctor.
    """
    doctor = session.get(Doctor, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    update_dict = doctor_in.model_dump(exclude_unset=True)
    doctor.sqlmodel_update(update_dict)
    session.add(doctor)
    session.commit()
    session.refresh(doctor)
    return doctor


@router.delete("/{doctor_id}", response_model=Message)
def delete_doctor(*, session: SessionDep, doctor_id: int) -> Message:
    """
    Delete a doctor.
    """
    doctor = session.get(Doctor, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    session.delete(doctor)
    session.commit()
    return Message(message="Doctor deleted successfully")
