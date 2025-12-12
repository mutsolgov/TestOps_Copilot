from app.domain.models import GenerationRequest, TestCase, TestType
from app.adapters.ai_client import AIProvider

class GenerationService:
    def __init__(self, ai_client: AIProvider):
        self.ai_client = ai_client

    async def generate_test_case(self, request: GenerationRequest) -> TestCase:
        prompt = self._construct_prompt(request)
        
        generated_code = await self.ai_client.generate_test_case(prompt)
        
        return TestCase(
            title=f"Test for {request.feature_description}",
            description=request.feature_description,
            steps=[],
            code=generated_code
        )

    def _construct_prompt(self, request: GenerationRequest) -> str:
        if request.is_manual:
            return self._manual_test_prompt(request)
        elif request.test_type == TestType.UI:
            return self._ui_autotest_prompt(request)
        else:
            return self._api_autotest_prompt(request)

    def _manual_test_prompt(self, request: GenerationRequest) -> str:
        return f"""
You are a Senior QA Automation Architect.
Generate a Python test case strictly following the "Allure TestOps as Code" standard.

INPUT:
User Requirements: {request.feature_description}
Owner: {request.owner}
Priority: {request.priority}
Test Type: {request.test_type}

STRICT OUTPUT RULES:
1. Return ONLY valid Python code. NO markdown formatting calls.
2. ANALYZE the {request.feature_description} deeply.
3. SPLIT the requirements into logical steps (Arrange -> Act -> Assert).
4. FOR EACH requirement, generate a specific `with allure.step("...")` block.
5. BAN: Do NOT use generic names like "Step 1", "Action", "Check result".
6. REQUIREMENT: The step title MUST contain the specific business logic (e.g., "Verify 'Add Service' button is visible", not just "Verify button").
7. Allure decorators are MANDATORY.

TEMPLATE (Example Structure - Fill with REAL content):
@allure.manual
@allure.label("owner", "{request.owner}")
@allure.feature("Feature Name")
@allure.story("Story Name")
@allure.suite("manual")
@mark.manual
class TestFeatureName:
    @allure.title("Test Title")
    @allure.tag("NORMAL")
    @allure.label("priority", "{request.priority}")
    def test_scenario(self) -> None:
        # Arrange
        with allure.step("Navigate to the main page"):
             # checks...
             pass
        
        # Act
        with allure.step("Click 'Add Service' button"):
             # actions...
             pass
            
        # Assert (Must match requirements)
        with allure.step("Verify total price is displayed with VAT"):
             # verifications...
             pass
"""

    def _ui_autotest_prompt(self, request: GenerationRequest) -> str:
        return f"""
You are a Senior QA Automation Architect.
Generate an ASYNC Playwright test using pytest and allure.

INPUT:
User Requirements: {request.feature_description}
Owner: {request.owner}

STRICT OUTPUT RULES:
1. Return ONLY valid Python code. NO markdown blocks.
2. Use AAA pattern (Arrange, Act, Assert).
3. Use async/await for all Playwright interactions.

TEMPLATE:
import pytest
from playwright.async_api import Page
import allure

@allure.feature("UI Feature")
@allure.story("User Story")
@allure.label("owner", "{request.owner}")
class TestUIFeature:
    @allure.title("Test Title")
    @pytest.mark.asyncio
    async def test_ui_flow(self, page: Page) -> None:
        # Arrange
        with allure.step("Open page"):
            await page.goto("https://example.com")
        
        # Act
        with allure.step("Interact"):
            await page.click("#submit")
            
        # Assert
        with allure.step("Verify"):
            await expect(page).to_have_title("Dashboard")
"""

    def _api_autotest_prompt(self, request: GenerationRequest) -> str:
        return f"""
You are a Senior QA Automation Architect.
Generate an API test using pytest and httpx (async).

INPUT:
User Requirements: {request.feature_description}
Owner: {request.owner}

STRICT OUTPUT RULES:
1. Return ONLY valid Python code. NO markdown blocks.
2. Use AAA pattern.

TEMPLATE:
import pytest
import httpx
import allure

@allure.feature("API Feature")
@allure.story("API Story")
@allure.label("owner", "{request.owner}")
class TestAPIFeature:
    @allure.title("Test Title")
    @pytest.mark.asyncio
    async def test_api_flow(self) -> None:
        async with httpx.AsyncClient() as client:
            # Arrange
            payload = {{"key": "value"}}
            
            # Act
            with allure.step("Send POST request"):
                response = await client.post("https://api.example.com/v1/resource", json=payload)
            
            # Assert
            with allure.step("Verify response"):
                assert response.status_code == 201
"""
