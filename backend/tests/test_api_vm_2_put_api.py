import pytest
import allure
import requests
import os

@allure.feature("VMStatusManagement")
@allure.story("Story: VMStatusManagement")
@allure.suite("API")
@allure.link("https://jira.cloud.ru/browse/TASK-API-VM-STATUS", name="API Docs")
class TestVMStatusManagement:
    @allure.title("API Test: Change VM Status")
    @allure.link("https://jira.cloud.ru/browse/TASK-PENDING", name="Related Task")
    @allure.tag("NORMAL")
    @allure.label("priority", "normal")
    def test_scenario(self):
        # Arrange
        base_url = "https://compute.api.cloud.ru"
        
        # Configuration
        vm_id = os.getenv("TEST_VM_ID")
        token = os.getenv("CLOUD_API_TOKEN") # Security fix
        
        # Validation
        assert vm_id, "Please set TEST_VM_ID in your .env file"

        vm_endpoint = f"/api/v1/vms/{vm_id}"
        bulk_endpoint = "/api/v1/vms"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Step 1: Get Current State
        with allure.step(f"GET {vm_endpoint}"):
            response_get = requests.get(base_url + vm_endpoint, headers=headers)
            assert response_get.status_code == 200, "Failed to get current VM info"
            current_state = response_get.json()["state"]
            
        # Step 2: Determine Target State
        target_state = "stopped" if current_state == "running" else "running"

        # Step 3: PUT New State (Bulk Endpoint)
        payload = [
          {
            "id": vm_id,
            "state": target_state
          }
        ]

        # Act
        with allure.step(f"PUT {bulk_endpoint} -> Switch to {target_state}"):
            response = requests.put(base_url + bulk_endpoint, headers=headers, json=payload)

        # Assert
        with allure.step("Check Status Code 204"):
            assert response.status_code == 204, f"Expected 204, got {response.status_code}"
        

