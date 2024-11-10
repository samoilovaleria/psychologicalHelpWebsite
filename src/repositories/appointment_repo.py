from sqlalchemy.exc import IntegrityError
from src.models.appointments_model import (
    Appointment,
    AppointmentType,
    AppointmentStatus
)

from src.config.database import get_async_db
from sqlalchemy.future import select
from sqlalchemy import insert
from uuid import UUID, uuid4
from datetime import datetime


async def get_appointment(appointment_id: UUID):
    async with get_async_db() as session:
        result = await session.execute(select(Appointment).filter(Appointment.id == appointment_id))
    return result.scalar_one_or_none()


async def create_appointment(
        patient_id: UUID,
        therapist_id: UUID,
        type: AppointmentType,
        reason: str | None,
        status: AppointmentStatus,
        remind_time: datetime | None,
        last_change_time: datetime,
        venue: str
):
    async with get_async_db() as session:
        new_appointment = Appointment(
            id=uuid4(),
            patient_id=patient_id,
            therapist_id=therapist_id,
            type=type,
            reason=reason,
            status=status,
            remind_time=remind_time,
            last_change_time=last_change_time,
            venue=venue
        )

        try:
            session.add(new_appointment)
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            raise ValueError(f"Ошибка при создании встречи: {e.orig}")
