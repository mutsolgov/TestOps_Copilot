import pytest
import allure
import requests
import os

@allure.feature("DiskDetailsAPI")
@allure.story("Story: DiskDetailsAPI")
@allure.suite("API")
@allure.link("https://jira.cloud.ru/browse/TASK-API-DISK-DETAILS", name="API Docs")
class TestDiskDetailsAPI:
    @allure.title("API Test: Get Disk Details")
    @allure.link("https://jira.cloud.ru/browse/TASK-PENDING", name="Related Task")
    @allure.tag("NORMAL")
    @allure.label("priority", "normal")
    def test_scenario(self):
        # Arrange
        base_url = "https://compute.api.cloud.ru"
        
        # Configuration
        disk_id = os.getenv("TEST_DISK_ID")
        token = os.getenv("CLOUD_API_TOKEN")
        
        # Validation
        assert disk_id, "Please set TEST_DISK_ID in your .env file"
        
        endpoint = f"/api/v1/disks/{disk_id}"
        
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
            assert data["id"] == disk_id, "ID mismatch"
            assert "name" in data, "Response missing 'name'"
            assert "size" in data, "Response missing 'size'"
            assert "state" in data, "Response missing 'state'"
            assert "created_time" in data, "Response missing 'created_time'"
            
        with allure.step("Validate Nested Objects"):
            assert "disk_type" in data, "Response missing 'disk_type'"
            assert "availability_zone" in data, "Response missing 'availability_zone'"
        

