from src.models.appointments_model import Appointment
from src.config.database import get_async_db
from sqlalchemy.future import select


async def get_appointment(appointment_id: int):
    async with get_async_db() as session:
        result = await session.execute(select(Appointment).filter(Appointment.id == appointment_id))
    return result.scalar_one_or_none()