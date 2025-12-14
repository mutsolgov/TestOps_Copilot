import pytest
import allure
import requests
import os

@allure.feature("FlavorsDetailsAPI")
@allure.story("Story: FlavorsDetailsAPI")
@allure.suite("API")
@allure.link("https://jira.cloud.ru/browse/TASK-API-FLAVORS-DETAILS", name="API Docs")
class TestFlavorsDetailsAPI:
    @allure.title("API Test: Get Flavor Details")
    @allure.link("https://jira.cloud.ru/browse/TASK-PENDING", name="Related Task")
    @allure.tag("NORMAL")
    @allure.label("priority", "normal")
    def test_scenario(self):
        # Arrange
        base_url = "https://compute.api.cloud.ru"
        
        # Configuration
        flavor_id = os.getenv("TEST_FLAVOR_ID")
        token = os.getenv("CLOUD_API_TOKEN")
        
        # Validation
        error_msg = "Please set TEST_FLAVOR_ID in your .env file"
        assert flavor_id, error_msg
        
        endpoint = f"/api/v1/flavors/{flavor_id}"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        # Act
        with allure.step(f"GET {endpoint}"):
            response = requests.get(base_url + endpoint, headers=headers)

        # Assert
        with allure.step("Check Status Code 200"):
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        
        with allure.step("Validate Response Schema"):
            assert "id" in data, "Response missing 'id'"
            assert data["id"] == flavor_id, "ID mismatch"
            assert "name" in data, "Response missing 'name'"
            assert "cpu" in data, "Response missing 'cpu'"
            assert "ram" in data, "Response missing 'ram'"
            assert "type" in data, "Response missing 'type'"
            assert "availability_zones" in data, "Response missing 'availability_zones'"
            assert isinstance(data["availability_zones"], list), "'availability_zones' must be a list"
        

