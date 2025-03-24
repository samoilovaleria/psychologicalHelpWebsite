from fastapi import APIRouter
from .controllers import users_routes
from .controllers import appointment_routes
from .controllers import reviews_routes
from .controllers import therapist_routes
from .controllers import roles_routes
from .controllers import images


api_router = APIRouter()
api_router.include_router(users_routes.router)
api_router.include_router(appointment_routes.router)
api_router.include_router(reviews_routes.router)
api_router.include_router(therapist_routes.router)
api_router.include_router(roles_routes.router)
api_router.include_router(images.router)
