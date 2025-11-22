# Backend/routers/donations.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Backend.models import Donation
from Backend.schemas import DonationOut, DonationCreate
from Backend.deps import get_db

router = APIRouter(tags=["Donations"])

@router.get("/available", response_model=list[DonationOut])
def list_available_donations(db: Session = Depends(get_db)):
    donations = (
        db.query(Donation)
        .filter(Donation.status == "AVAILABLE")
        .order_by(Donation.expires_at)
        .all()
    )
    return donations


@router.post("/create", response_model=DonationOut)
def create_donation(payload: DonationCreate, db: Session = Depends(get_db)):
    try:
        donation = Donation(
            donor_user_id=1, # Replace with token later
            category_id=payload.category_id,
            description=payload.description,
            quantity=payload.quantity,
            unit=payload.unit,
            expires_at=payload.expires_at,
            pickup_address=payload.pickup_address,
            city=payload.city,
            state=payload.state,
            zip_code=payload.zip_code,
            status="AVAILABLE"
        )
        db.add(donation)
        db.commit()
        db.refresh(donation)
        return donation

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
