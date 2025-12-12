from typing import Generator, Annotated
from fastapi import Depends
from app.adapters.ai_client import get_ai_provider, AIProvider
from app.services.generator import GenerationService
from app.services.validator import ValidationService

def get_generation_service(
    ai_client: Annotated[AIProvider, Depends(get_ai_provider)]
) -> GenerationService:
    return GenerationService(ai_client)

def get_validation_service() -> ValidationService:
    return ValidationService()
