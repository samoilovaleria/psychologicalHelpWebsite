from fastapi import HTTPException, APIRouter, Query, Request

from psychohelp.services.therapists import get_therapist_by_id, get_therapists as srv_get_therapists, UUID
from psychohelp.schemas.therapists import TherapistBase

router = APIRouter(prefix="/therapists", tags=["therapists"])


@router.get("/{therapist_id}", response_model=TherapistBase)
async def get_therapist(therapist_id: UUID):
    appointment = await get_therapist_by_id(therapist_id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Therapist not found")
    return appointment


@router.get("/", response_model=list[TherapistBase])
async def get_therapists(
    request: Request, skip: int = Query(0, ge=0), take: int = Query(10, gt=0)
):
    """
    Получить список психологов с пагинацией
    """
    therapists = await srv_get_therapists(skip=skip, take=take)
    if not therapists:
        raise HTTPException(status_code=404, detail="No therapists found")
    return therapists
