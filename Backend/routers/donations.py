# backend/routers/donations.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..deps import get_db, get_current_user
from .. import models

router = APIRouter(prefix="/donations", tags=["Donations"])


@router.get("/", summary="List all donations (simple example)")
def list_donations(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Example endpoint that requires a valid JWT token.
    For now it just returns basic fields from Donation.
    """
    donations = db.execute(
        "SELECT donation_id, title, quantity, unit, status FROM Donation"
    ).fetchall()
    return [
        {
            "donation_id": row.donation_id,
            "title": row.title,
            "quantity": float(row.quantity),
            "unit": row.unit,
            "status": row.status,
        }
        for row in donations
    ]
