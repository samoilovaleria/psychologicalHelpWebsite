from fastapi import HTTPException

from psychohelp.repositories.appointment_repo import (
    get_appointment,
    create_appointment as db_create_appointment,
    cancel_appointment,
    get_appointments_by_user_id,
)

from psychohelp.repositories.therapist_repo import get_therapist
from psychohelp.repositories.roles_repo import get_role_by_user_id
from psychohelp.repositories.helpers import get_user_email_from_token
from psychohelp.repositories.users_repo import (
    get_user_by_email as repo_get_user_by_email,
)

from models.roles_model import UserRole
from models.appointments_model import AppointmentType, AppointmentStatus

from uuid import UUID
from datetime import datetime


async def get_appointment_by_id(appointment_id: UUID):
    return await get_appointment(appointment_id)


async def create_appointment(appointment_data):
    now = datetime.now()
    remind_time = None
    if appointment_data.remind_time is not None:
        remind_time = datetime.fromisoformat(appointment_data.remind_time)
    status = AppointmentStatus.Accepted
    venue = appointment_data.venue

    role = await get_role_by_user_id(appointment_data.therapist_id)
    if role.role != UserRole.Therapist:
        raise ValueError("The therapist has no therapist role")

    role = await get_role_by_user_id(appointment_data.patient_id)
    if role.role not in (UserRole.Student, UserRole.Stuff):
        raise ValueError("The patient has no patient roles")

    # Встречаемся лично на месте работы психолога
    if appointment_data.type == AppointmentType.Offline:
        therapist = await get_therapist(appointment_data.therapist_id)
        venue = therapist.office

    elif venue is None:
        raise ValueError("Место для онлайн встречи не указано")

    result = await db_create_appointment(
        appointment_data.patient_id,
        appointment_data.therapist_id,
        appointment_data.type,
        appointment_data.reason,
        status,
        remind_time,
        now,
        venue,
    )

    return result


async def cancel_appointment_by_id(appointment_id: UUID):
    try:
        appointment = await cancel_appointment(appointment_id)
        return appointment
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_appointments_by_token(token: str):
    try:
        email = await get_user_email_from_token(token)
        user = await repo_get_user_by_email(email)
        if not user:
            raise ValueError("User not found")

        appointments = await get_appointments_by_user_id(user.id)
        return appointments
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
