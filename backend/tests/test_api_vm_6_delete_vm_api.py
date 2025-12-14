import pytest
import allure
import requests
import os

@allure.feature("VMDeletionAPI")
@allure.story("Story: VMDeletionAPI")
@allure.suite("API")
@allure.link("https://jira.cloud.ru/browse/TASK-API-VM-DELETE", name="API Docs")
class TestVMDeletionAPI:
    @allure.title("API Test: Delete VM")
    @allure.link("https://jira.cloud.ru/browse/TASK-PENDING", name="Related Task")
    @allure.tag("NORMAL")
    @allure.label("priority", "normal")
    def test_scenario(self):
        # Arrange
        base_url = "https://compute.api.cloud.ru"
        
        # Configuration
        vm_id = os.getenv("TEST_VM_ID_DEL")
        disk_id = os.getenv("TEST_DISK_VM_ID_DEL")
        external_ips = os.getenv("TEST_EXTERNAL_IPS") # если ip нет оставьте просто []
        token = os.getenv("CLOUD_API_TOKEN")
        
        # Validation
        error_msg = "Please set TEST_VM_ID, TEST_DISK_VM_ID and TEST_EXTERNAL_IPS in your .env file"
        assert vm_id, error_msg
        assert disk_id, error_msg
        assert external_ips is not None, error_msg

        endpoint = f"/api/v1/vms/{vm_id}"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Process external_ips string to list
        ips_list = [ip.strip() for ip in external_ips.split(',')] if external_ips else []
        
        payload = {
          "delete_attachments": {
            "disk_ids": [disk_id],
            "external_ips": ips_list
          }
        }

        # Act
        with allure.step(f"DELETE {endpoint}"):
            response = requests.request("DELETE", base_url + endpoint, headers=headers, json=payload)

        # Assert
        with allure.step("Check Status Code 204"):
            assert response.status_code == 204, f"Expected 204, got {response.status_code}"
        

