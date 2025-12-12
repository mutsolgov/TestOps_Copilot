from fastapi import APIRouter, Depends
from app.domain.models import GenerationRequest, TestCase, ValidationResult
from app.api.deps import get_generation_service, get_validation_service
from app.services.generator import GenerationService
from app.services.validator import ValidationService

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Welcome to TestOps Copilot API"}

@router.post("/generate", response_model=TestCase)
async def generate_test_case(
    request: GenerationRequest,
    service: GenerationService = Depends(get_generation_service)
):
    return await service.generate_test_case(request)

@router.post("/validate", response_model=ValidationResult)
async def validate_test_case(
    code: str,
    service: ValidationService = Depends(get_validation_service)
):
    return service.validate_code(code)
