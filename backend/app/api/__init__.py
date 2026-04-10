# API module
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.books import router as books_router
from app.api.reservations import router as reservations_router
from app.api.exchange_points import router as exchange_points_router
from app.api.reviews import router as reviews_router
from app.api.files import router as files_router
from app.api.statistics import router as statistics_router
from app.api.permissions import router as permissions_router
from app.api.external import router as external_router
from app.api.seo import router as seo_router

__all__ = [
    "auth_router",
    "users_router",
    "books_router",
    "reservations_router",
    "exchange_points_router",
    "reviews_router",
    "files_router",
    "statistics_router",
    "permissions_router",
    "external_router",
    "seo_router",
]
