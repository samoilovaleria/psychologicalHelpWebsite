from models.therapists_model import Therapist
from config.database import get_async_db
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import selectinload
from uuid import UUID


async def get_therapist(therapist_id: UUID):
    async with get_async_db() as session:
        result = await session.execute(
            select(Therapist)
            .options(selectinload(Therapist.user))  # Загружаем связанные данные сразу
            .filter(Therapist.id == therapist_id)
        )
        therapist = result.scalar_one_or_none()

    return therapist  # Возвращаем загруженный объект

async def get_therapists_with_pagination(skip: int = 0, take: int = 10):
    """
    Получить список психологов с пагинацией
    """
    async with get_async_db() as session:
        query = await session.execute(
            select(Therapist)
            .options(joinedload(Therapist.user))  # Загрузка связанных данных из модели User
            .offset(skip)
            .limit(take)
        )

    result = query.scalars().all()
    return result
