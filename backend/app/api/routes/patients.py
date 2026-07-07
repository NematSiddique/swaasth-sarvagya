from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.api.deps import SessionDep
from app.models import Message, Patient

router = APIRouter(prefix="/patients", tags=["patients"])


@router.post("/", response_model=Patient)
def create_patient(*, session: SessionDep, patient_in: Patient) -> Any:
    """
    Create new patient.
    """
    patient = Patient.model_validate(patient_in)
    session.add(patient)
    session.commit()
    session.refresh(patient)
    return patient


@router.get("/", response_model=list[Patient])
def read_patients(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve patients.
    """
    statement = select(Patient).offset(skip).limit(limit)
    patients = session.exec(statement).all()
    return patients


@router.get("/{patient_id}", response_model=Patient)
def read_patient(*, session: SessionDep, patient_id: int) -> Any:
    """
    Get patient by ID.
    """
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.put("/{patient_id}", response_model=Patient)
def update_patient(*, session: SessionDep, patient_id: int, patient_in: Patient) -> Any:
    """
    Update a patient.
    """
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    update_dict = patient_in.model_dump(exclude_unset=True)
    patient.sqlmodel_update(update_dict)
    session.add(patient)
    session.commit()
    session.refresh(patient)
    return patient


@router.delete("/{patient_id}", response_model=Message)
def delete_patient(*, session: SessionDep, patient_id: int) -> Message:
    """
    Delete a patient.
    """
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    session.delete(patient)
    session.commit()
    return Message(message="Patient deleted successfully")
