from src.models.reviews_model import Review
from src.config.database import get_async_db
from sqlalchemy.future import select


async def get_review(appointment_id: int):
    async with get_async_db() as session:
        result = await session.execute(select(Review).filter(Review.appointment_id == appointment_id))
    return result.scalar_one_or_none()