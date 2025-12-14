import pytest
import allure
import requests
import os
import time

@allure.feature("VMUpdateAPI")
@allure.story("Story: VMUpdateAPI")
@allure.suite("API")
@allure.link("https://jira.cloud.ru/browse/TASK-API-VM-UPDATE", name="API Docs")
class TestVMUpdateAPI:
    @allure.title("API Test: Update VM")
    @allure.link("https://jira.cloud.ru/browse/TASK-PENDING", name="Related Task")
    @allure.tag("NORMAL")
    @allure.label("priority", "normal")
    def test_scenario(self):
        # Arrange
        base_url = "https://compute.api.cloud.ru"
        vm_id = "a4a95988-3907-4724-ad06-a7bd42ac5680" # Example UUID
        endpoint = f"/api/v1/vms/{vm_id}"
        token = os.getenv("CLOUD_API_TOKEN") # Security fix
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "name": f"Updated Name {int(time.time())}", # Добавьте уникальность
            "description": "Updated Description via Test",
            # ИСПРАВЛЕНИЕ: Используем UUID, а не имя!
            "flavor_id": "139ddd16-2482-4694-991d-9b1834266e03", 
            # ДОБАВЛЕНИЕ: Project ID часто обязателен для PUT
            "project_id": "4582273a-e0e7-4fb4-b284-8a91cb03d106" 
        }

        # Act
        with allure.step(f"PUT {endpoint}"):
            response = requests.put(base_url + endpoint, headers=headers, json=payload)

        # Assert
        with allure.step("Check Status Code 200"):
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        
        with allure.step("Validate Response Structure"):
            assert isinstance(data, dict), "Response should be a JSON Object"
            assert data["id"] == vm_id, "ID should match"
            assert "name" in data
        

