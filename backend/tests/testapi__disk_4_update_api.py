import pytest
import allure
import requests
import os

@allure.feature("DiskUpdateAPI")
@allure.story("Story: DiskUpdateAPI")
@allure.suite("API")
@allure.link("https://jira.cloud.ru/browse/TASK-API-DISK-UPDATE", name="API Docs")
class TestDiskUpdateAPI:
    @allure.title("API Test: Update Disk")
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
        
        # Dynamic Payload
        import time
        unique_suffix = int(time.time())
        payload = {
            "name": f"updated-disk-{unique_suffix}",
            "description": "Updated description",
            "size": 10, # Size must be >= current size, assume 10 is safe or equal
            "readonly": False,
            "shared": False,
            "encrypted": False
        }

        # Act
        with allure.step(f"PUT {endpoint}"):
            response = requests.put(base_url + endpoint, headers=headers, json=payload)

        # Assert
        with allure.step("Check Status Code 200"):
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        
        with allure.step("Validate Response Schema"):
            assert data["id"] == disk_id, "ID mismatch"
            assert data["name"] == payload["name"], "Name not updated"
            assert data["description"] == payload["description"], "Description not updated"
            assert "state" in data
            assert "created_time" in data
            
        with allure.step("Validate Nested Objects"):
             assert "disk_type" in data
             assert "availability_zone" in data
