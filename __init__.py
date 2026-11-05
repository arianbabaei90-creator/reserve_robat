from aiogram import Router
from . import start, booking, my_appointments, admin


def setup_routers() -> Router:
    main_router = Router()
    main_router.include_router(start.router)
    main_router.include_router(booking.router)
    main_router.include_router(my_appointments.router)
    main_router.include_router(admin.router)
    return main_router