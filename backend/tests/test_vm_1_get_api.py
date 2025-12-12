import pytest
import allure
import requests
import os

@allure.feature("VirtualMachinesAPI")
@allure.story("Story: VirtualMachinesAPI")
@allure.suite("API")
@allure.link("https://jira.cloud.ru/browse/TASK-API-VMS", name="API Docs")
class TestVirtualMachinesAPI:
    @allure.title("API Test: Get VM List")
    @allure.link("https://jira.cloud.ru/browse/TASK-PENDING", name="Related Task")
    @allure.tag("NORMAL")
    @allure.label("priority", "normal")
    def test_scenario(self):
        # Arrange
        base_url = "https://compute.api.cloud.ru"
        endpoint = "/api/v1/vms"
        
        # Configuration
        project_id = os.getenv("TEST_PROJECT_ID")
        token = os.getenv("CLOUD_API_TOKEN") # Security fix
        
        # Validation
        assert project_id, "Please set TEST_PROJECT_ID in your .env file"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        params = {
            "project_id": project_id,
            "limit": 50
        }

        # Act
        with allure.step(f"GET {endpoint}"):
            response = requests.get(base_url + endpoint, headers=headers, params=params)

        # Assert
        with allure.step("Check Status Code 200"):
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        
        with allure.step("Validate Response Schema"):
            assert "items" in data, "Response missing 'items' field"
            assert "total" in data, "Response missing 'total' field"
            assert isinstance(data["items"], list), "'items' must be a list"
            
        with allure.step("Validate Item Structure"):
            if data["items"]:
                item = data["items"][0]
                assert "id" in item
                assert "name" in item
                assert "state" in item
