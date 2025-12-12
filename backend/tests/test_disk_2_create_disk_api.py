import pytest
import allure
import requests
import os

@allure.feature("DisksCreateAPI")
@allure.story("Story: DisksCreateAPI")
@allure.suite("API")
@allure.link("https://jira.cloud.ru/browse/TASK-API-DISKS-CREATE", name="API Docs")
class TestDisksCreateAPI:
    @allure.title("API Test: Create Disk")
    @allure.link("https://jira.cloud.ru/browse/TASK-PENDING", name="Related Task")
    @allure.tag("NORMAL")
    @allure.label("priority", "normal")
    def test_scenario(self):
        # Arrange
        base_url = "https://compute.api.cloud.ru"
        endpoint = "/api/v1/disks"
        
        # Configuration
        project_id = os.getenv("TEST_PROJECT_ID")
        token = os.getenv("CLOUD_API_TOKEN")
        
        # Validation
        assert project_id, "Please set TEST_PROJECT_ID in your .env file"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Dynamic payload with unique name to avoid 409
        import time
        unique_suffix = int(time.time())
        
        payload = {
            "project_id": project_id,
            "name": f"test-disk-{unique_suffix}",
            "description": "Auto-generated test disk",
            "size": 10
        }

        # Act
        with allure.step(f"POST {endpoint}"):
            response = requests.post(base_url + endpoint, headers=headers, json=payload)

        # Assert
        with allure.step("Check Status Code 201"):
            assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        
        data = response.json()
        
        with allure.step("Validate Response Schema"):
            assert "id" in data, "Response missing 'id'"
            assert data["name"] == payload["name"], "Name mismatch"
            assert data["size"] == payload["size"], "Size mismatch"
            assert "state" in data, "Response missing 'state'"
            assert "created_time" in data, "Response missing 'created_time'"
        

