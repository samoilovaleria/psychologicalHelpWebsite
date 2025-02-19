from fastapi import HTTPException, APIRouter
from uuid import UUID
from services.review_service import get_review_by_id
from schemas.reviews_schema import ReviewsBase

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.get("/{appointment_id}", response_model=ReviewsBase)
async def read_appointment(appointment_id: UUID):
    appointment = await get_review_by_id(appointment_id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return appointment
