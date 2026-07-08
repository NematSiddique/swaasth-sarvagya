from fastapi import APIRouter

from app.api.routes import diseases, doctors, hospitals, medicines, patients

api_router = APIRouter()

api_router.include_router(hospitals.router)
api_router.include_router(doctors.router)
api_router.include_router(patients.router)
api_router.include_router(medicines.router)
api_router.include_router(diseases.router)
