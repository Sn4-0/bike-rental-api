from fastapi import APIRouter

from .bicycle import router as bicycles_router
from .location import router as locations_router
from .user import router as users_router
from .rental import router as rentals_router
from .discount import router as discounts_router


api_router = APIRouter()

api_router.include_router(bicycles_router)
api_router.include_router(locations_router)
api_router.include_router(users_router)
api_router.include_router(rentals_router)
api_router.include_router(discounts_router)
