from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional

class TestType(str, Enum):
    UI = "ui"
    API = "api"

class GenerationRequest(BaseModel):
    feature_description: str
    test_type: TestType
    owner: str = "qa_user"
    priority: str = "normal"
    is_manual: bool = True

class TestCaseStep(BaseModel):
    title: str
    action: str
    expected_result: str

class TestCase(BaseModel):
    title: str
    description: str
    steps: List[TestCaseStep]
    tags: List[str] = []
    code: Optional[str] = None

class ValidationResult(BaseModel):
    is_valid: bool
    errors: List[str] = []
    fixed_code: Optional[str] = None
