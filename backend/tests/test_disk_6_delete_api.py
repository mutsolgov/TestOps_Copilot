import pytest
import allure
import requests
import os

@allure.feature("DiskDeleteAPI")
@allure.story("Story: DiskDeleteAPI")
@allure.suite("API")
@allure.link("https://jira.cloud.ru/browse/TASK-API-DISK-DELETE", name="API Docs")
class TestDiskDeleteAPI:
    @allure.title("API Test: Delete Disk")
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
        }

        # Act
        with allure.step(f"DELETE {endpoint}"):
            response = requests.delete(base_url + endpoint, headers=headers)

        # Assert
        with allure.step("Check Status Code 204"):
            assert response.status_code == 204, f"Expected 204, got {response.status_code}"
        

