from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.api.deps import get_db
from app.models import Forecast, ForecastPublic, Message

router = APIRouter()


@router.get("/forecasts/", response_model=list[ForecastPublic])
def read_forecasts(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve forecasts.
    """
    forecasts = db.query(Forecast).offset(skip).limit(limit).all()
    return forecasts


@router.post("/ai/ask", response_model=Message)
def ask_ai(
    *,
    db: Session = Depends(get_db),
    message: Message,
) -> Any:
    """
    Send a message to the Gemini AI assistant.

    This is a placeholder. In a real implementation, this would:
    1. Construct a detailed prompt with context from the database (e.g., active alerts).
    2. Call the Gemini API.
    3. Return the processed response.
    """
    if not message.content:
        raise HTTPException(status_code=400, detail="Message content cannot be empty.")

    # Placeholder response
    return Message(content=f"AI response to: '{message.content}'")
