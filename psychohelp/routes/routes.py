from fastapi import APIRouter
from .controllers import users
from .controllers import appointments
from .controllers import reviews
from .controllers import therapists
from .controllers import images


api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(appointments.router)
api_router.include_router(reviews.router)
api_router.include_router(therapists.router)
api_router.include_router(images.router)
