from fastapi import APIRouter

from app.api import charityproject_router, donation_router, user_router

main_router = APIRouter()
main_router.include_router(
    charityproject_router, prefix='/charity_project', tags=['Charity project']
)
main_router.include_router(
    donation_router, prefix='/donation', tags=['Donation']
)

main_router.include_router(user_router)
