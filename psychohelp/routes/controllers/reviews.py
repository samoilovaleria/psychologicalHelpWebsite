from fastapi import HTTPException, APIRouter

from psychohelp.services.reviews import get_review_by_id, UUID
from psychohelp.schemas.reviews import ReviewsBase


router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.get("/{review_id}", response_model=ReviewsBase)
async def get_review(review_id: UUID):
    review = await get_review_by_id(review_id)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return review
