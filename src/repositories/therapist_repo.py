from src.models.therapists_model import Therapist
from src.config.database import get_async_db
from sqlalchemy.future import select
from uuid import UUID


async def get_therapist(therapist_id: UUID):
    async with get_async_db() as session:
        result = await session.execute(select(Therapist).filter(Therapist.id == therapist_id))
    return result.scalar_one_or_none()