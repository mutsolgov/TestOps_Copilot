import pytest
import allure
import requests
import os

@allure.feature("VMDetailsAPI")
@allure.story("Story: VMDetailsAPI")
@allure.suite("API")
@allure.link("https://jira.cloud.ru/browse/TASK-API-VM-DETAILS", name="API Docs")
class TestVMDetailsAPI:
    @allure.title("API Test: Get VM Details")
    @allure.link("https://jira.cloud.ru/browse/TASK-PENDING", name="Related Task")
    @allure.tag("NORMAL")
    @allure.label("priority", "normal")
    def test_scenario(self):
        # Arrange
        base_url = "https://compute.api.cloud.ru"
        
        # Configuration
        vm_id = os.getenv("TEST_VM_ID")
        
        # Validation
        assert vm_id, "Please set TEST_VM_ID in your .env file"

        endpoint = f"/api/v1/vms/{vm_id}"
        token = os.getenv("CLOUD_API_TOKEN") # Security fix
        
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
        
        with allure.step("Validate Response Structure (Object)"):
            assert isinstance(data, dict), "Response should be a JSON Object"
            assert "id" in data
            assert "name" in data
            assert "state" in data
            assert "flavor" in data
            assert "interfaces" in data
        
        with allure.step("Validate Nested Objects"):
             if "flavor" in data:
                 assert "id" in data["flavor"]
                 assert "cpu" in data["flavor"]
        

