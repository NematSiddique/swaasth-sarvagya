from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.api.deps import SessionDep
from app.models import Medicine, Message

router = APIRouter(prefix="/medicines", tags=["medicines"])


@router.post("/", response_model=Medicine)
def create_medicine(*, session: SessionDep, medicine_in: Medicine) -> Any:
    """
    Create new medicine.
    """
    medicine = Medicine.model_validate(medicine_in)
    session.add(medicine)
    session.commit()
    session.refresh(medicine)
    return medicine


@router.get("/", response_model=list[Medicine])
def read_medicines(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve medicines.
    """
    statement = select(Medicine).offset(skip).limit(limit)
    medicines = session.exec(statement).all()
    return medicines


@router.get("/{medicine_id}", response_model=Medicine)
def read_medicine(*, session: SessionDep, medicine_id: int) -> Any:
    """
    Get medicine by ID.
    """
    medicine = session.get(Medicine, medicine_id)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return medicine


@router.put("/{medicine_id}", response_model=Medicine)
def update_medicine(
    *, session: SessionDep, medicine_id: int, medicine_in: Medicine
) -> Any:
    """
    Update a medicine.
    """
    medicine = session.get(Medicine, medicine_id)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    update_dict = medicine_in.model_dump(exclude_unset=True)
    medicine.sqlmodel_update(update_dict)
    session.add(medicine)
    session.commit()
    session.refresh(medicine)
    return medicine


@router.delete("/{medicine_id}", response_model=Message)
def delete_medicine(*, session: SessionDep, medicine_id: int) -> Message:
    medicine = session.get(Medicine, medicine_id)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    session.delete(medicine)
    session.commit()
    return Message(message="Medicine deleted successfully")
