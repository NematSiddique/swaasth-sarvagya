from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.api.deps import SessionDep
from app.models import Disease, Message

router = APIRouter(prefix="/diseases", tags=["diseases"])


@router.post("/", response_model=Disease)
def create_disease(*, session: SessionDep, disease_in: Disease) -> Any:
    """
    Create new disease.
    """
    disease = Disease.model_validate(disease_in)
    session.add(disease)
    session.commit()
    session.refresh(disease)
    return disease


@router.get("/", response_model=list[Disease])
def read_diseases(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve diseases.
    """
    statement = select(Disease).offset(skip).limit(limit)
    diseases = session.exec(statement).all()
    return diseases


@router.get("/{disease_id}", response_model=Disease)
def read_disease(*, session: SessionDep, disease_id: int) -> Any:
    """
    Get disease by ID.
    """
    disease = session.get(Disease, disease_id)
    if not disease:
        raise HTTPException(status_code=404, detail="Disease not found")
    return disease


@router.put("/{disease_id}", response_model=Disease)
def update_disease(*, session: SessionDep, disease_id: int, disease_in: Disease) -> Any:
    """
    Update a disease.
    """
    disease = session.get(Disease, disease_id)
    if not disease:
        raise HTTPException(status_code=404, detail="Disease not found")
    update_dict = disease_in.model_dump(exclude_unset=True)
    disease.sqlmodel_update(update_dict)
    session.add(disease)
    session.commit()
    session.refresh(disease)
    return disease


@router.delete("/{disease_id}", response_model=Message)
def delete_disease(*, session: SessionDep, disease_id: int) -> Message:
    """
    Delete a disease.
    """
    disease = session.get(Disease, disease_id)
    if not disease:
        raise HTTPException(status_code=404, detail="Disease not found")
    session.delete(disease)
    session.commit()
    return Message(message="Disease deleted successfully")
