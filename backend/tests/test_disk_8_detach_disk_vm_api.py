import pytest
import allure
import requests
import os

@allure.feature("DiskDetachAPI")
@allure.story("Story: DiskDetachAPI")
@allure.suite("API")
@allure.link("https://jira.cloud.ru/browse/TASK-API-DISK-DETACH", name="API Docs")
class TestDiskDetachAPI:
    @allure.title("API Test: Detach Disk from VM")
    @allure.link("https://jira.cloud.ru/browse/TASK-PENDING", name="Related Task")
    @allure.tag("NORMAL")
    @allure.label("priority", "normal")
    def test_scenario(self):
        # Arrange
        base_url = "https://compute.api.cloud.ru"
        
        # Configuration
        disk_id = os.getenv("TEST_DISK_ID")
        vm_id = os.getenv("TEST_VM_ID")
        token = os.getenv("CLOUD_API_TOKEN")
        
        # Validation
        error_msg = "Please set TEST_DISK_ID and TEST_VM_ID in your .env file"
        assert disk_id, error_msg
        assert vm_id, error_msg
        
        endpoint = f"/api/v1/disks/{disk_id}/detach"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "vm_id": vm_id
        }

        # Act
        with allure.step(f"POST {endpoint}"):
            response = requests.post(base_url + endpoint, headers=headers, json=payload)

        # Assert
        with allure.step("Check Status Code 200"):
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        
        with allure.step("Validate Response Schema"):
            assert "id" in data, "Response missing 'id'"
            assert data["id"] == disk_id, "ID mismatch"
            assert "vms" in data, "Response missing 'vms' list"
            assert isinstance(data["vms"], list), "'vms' must be a list"

        with allure.step("Validate Detachment"):
            # Check if the VM is NO LONGER in the 'vms' list
            attached_vm_ids = [vm["id"] for vm in data["vms"]]
            assert vm_id not in attached_vm_ids, f"VM {vm_id} should be detached but found in list"
        

