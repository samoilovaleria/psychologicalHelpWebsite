from psychohelp.models.therapists import Therapist
from psychohelp.config.database import get_async_db

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import selectinload

from uuid import UUID


async def get_therapist_by_id(therapist_id: UUID):
    async with get_async_db() as session:
        result = await session.execute(
            select(Therapist)
            .options(selectinload(Therapist.user))
            .filter(Therapist.id == therapist_id)
        )
        therapist = result.scalar_one_or_none()

    return therapist


async def get_therapists(skip: int = 0, take: int = 10):
    """
    Получить список психологов с пагинацией
    """
    async with get_async_db() as session:
        query = await session.execute(
            select(Therapist)
            .options(joinedload(Therapist.user))
            .offset(skip)
            .limit(take)
        )

    result = query.scalars().all()
    return result
