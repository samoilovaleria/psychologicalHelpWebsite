import pytest
from uuid import uuid4
from datetime import datetime
from models.appointments_model import AppointmentType, AppointmentStatus

async def test_cancel_appointment(client, test_db):
    # Создаем тестовую запись
    appointment_data = {
        "patient_id": str(uuid4()),
        "therapist_id": str(uuid4()),
        "type": AppointmentType.Online,
        "reason": "Test appointment",
        "status": AppointmentStatus.Approved,
        "remind_time": datetime.utcnow().isoformat(),
        "last_change_time": datetime.utcnow().isoformat(),
        "venue": "Online"
    }
    
    # Создаем запись
    response = await client.post("/appointments/create", json=appointment_data)
    assert response.status_code == 200
    appointment_id = response.json()["appointment_id"]
    
    # Отменяем запись
    response = await client.put(f"/appointments/{appointment_id}/cancel")
    assert response.status_code == 200
    
    # Проверяем, что статус изменился
    response = await client.get(f"/appointments/{appointment_id}")
    assert response.status_code == 200
    assert response.json()["status"] == AppointmentStatus.Cancelled
