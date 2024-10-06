from sqlalchemy.orm import Session
from src.models.user_model import User
from sqlalchemy.future import select
from src.config.database import get_db
from src.config.database import get_async_db
from sqlalchemy.ext.asyncio import AsyncSession

# def get_user(user_id: int):
#     # , db: Session = Depends(get_db)
#     # return db.query(User).filter(User.id == user_id).first()

#     # with self._session_factory() as session:
#     with get_db() as session:
#         user = session.query(User).filter(User.id == user_id).first()
#     return user



async def get_user(user_id: int):
    async with get_async_db() as session:
        result = await session.execute(select(User).filter(User.id == user_id))
    return result.scalar_one_or_none()
