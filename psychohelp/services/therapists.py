from psychohelp.repositories.therapists import (
    get_therapist,
    get_therapists_with_pagination,
    UUID,
)


async def get_therapist_by_id(therapist_id: UUID):
    therapist = await get_therapist(therapist_id)

    if therapist is None:
        return None

    return {
        "id": str(therapist.id),
        "experience": therapist.experience,
        "qualification": therapist.qualification,
        "consult_areas": therapist.consult_areas,
        "description": therapist.description,
        "office": therapist.office,
        "first_name": therapist.user.first_name,
        "middle_name": therapist.user.middle_name,
        "last_name": therapist.user.last_name,
        "phone_number": therapist.user.phone_number,
        "email": therapist.user.email,
        "education": therapist.education,
        "short_description": therapist.short_description,
        "photo": therapist.photo,
    }


async def get_all_therapists(skip: int = 0, take: int = 10):
    """
    Получить список всех психологов с пагинацией
    """

    therapists = await get_therapists_with_pagination(skip=skip, take=take)
    return [
        {
            "id": str(therapist.id),
            "experience": therapist.experience,
            "qualification": therapist.qualification,
            "consult_areas": therapist.consult_areas,
            "description": therapist.description,
            "office": therapist.office,
            "first_name": therapist.user.first_name,
            "middle_name": therapist.user.middle_name,
            "last_name": therapist.user.last_name,
            "phone_number": therapist.user.phone_number,
            "email": therapist.user.email,
            "education": therapist.education,
            "short_description": therapist.short_description,
            "photo": therapist.photo,
        }
        for therapist in therapists
    ]
