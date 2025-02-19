from repositories.appointment_repo import (
    AppointmentType,
    AppointmentStatus
)

from pydantic import BaseModel

from uuid import UUID
from datetime import datetime


class AppointmentBase(BaseModel):
    patient_id: UUID
    therapist_id: UUID
    type: AppointmentType
    reason: str | None = None
    status: AppointmentStatus
    remind_time: datetime | None = None
    last_change_time: datetime
    venue: str


class AppointmentCreateRequest(BaseModel):
    patient_id: UUID
    therapist_id: UUID
    type: AppointmentType
    reason: str | None = None
    remind_time: str | None = None
    venue: str | None = None


class AppointmentCreateResponse(BaseModel):
    appointment_id: UUID
