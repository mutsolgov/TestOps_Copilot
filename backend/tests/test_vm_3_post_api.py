import pytest
import allure
import requests
import os

@allure.feature("VMCreationAPI")
@allure.story("Story: VMCreationAPI")
@allure.suite("API")
@allure.link("https://jira.cloud.ru/browse/TASK-API-VM-CREATE", name="API Docs")
class TestVMCreationAPI:
    @allure.title("API Test: Create VM")
    @allure.link("https://jira.cloud.ru/browse/TASK-PENDING", name="Related Task")
    @allure.tag("NORMAL")
    @allure.label("priority", "normal")
    def test_scenario(self):
        # Arrange
        base_url = "https://compute.api.cloud.ru"
        endpoint = "/api/v1/vms"
        token = os.getenv("CLOUD_API_TOKEN") # Security fix
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Payload: Array of objects (as per docs)
        payload = [
          {
            "project_id": "4582273a-e0e7-4fb4-b284-8a91cb03d106",
            "name": "test-vm-01",
            "flavor_id": "fa3e89aa-6829-47f5-8bf4-76d57211a9f1",
            "image_id": "84c230fd-5520-4984-8119-37365b66fd80",
            # Required array fields
            "disks": [
                {
                    "disk_id": "9fb32f13-bddc-42b3-9a07-4aed1801aae6",
                    "disk_name": "boot-disk"
                }
            ],
            # Optional fields populated from sample
            "description": "Auto-generated test VM",
            "cloud_init": "#!/bin/bash\necho hello"
          }
        ]

        # Act
        with allure.step(f"POST {endpoint}"):
            response = requests.post(base_url + endpoint, headers=headers, json=payload)

        # Assert
        with allure.step("Check Status Code 201 (Created)"):
            assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        
        data = response.json()
        
        with allure.step("Validate Response Schema"):
            # Check for Array response (as per docs: Response Code 201 -> Array)
            assert isinstance(data, list), "Response should be a list"
            if data:
                vm = data[0]
                assert "id" in vm, "Missing 'id'"
                assert "state" in vm, "Missing 'state'"
        
