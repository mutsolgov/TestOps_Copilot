import pytest
import allure
import requests
import os
import json


@pytest.fixture(scope="function")
def created_disk_data():
    base_url = "https://compute.api.cloud.ru"
    endpoint = "/api/v1/disks"
    
    # Configuration
    project_id = os.getenv("TEST_PROJECT_ID")
    az_id = os.getenv("TEST_AZ_ID", "479a4ab3-3ff3-4972-95c5-7610bac5c0bb")
    disk_type_id = os.getenv("TEST_DISK_TYPE_ID", "a859e3dc-6b14-42a8-9bcc-890fde0ba6d0")
    token = os.getenv("CLOUD_API_TOKEN")
    
    assert project_id, "Please set TEST_PROJECT_ID in your .env file"
    assert token, "Please set CLOUD_API_TOKEN in your .env file"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Dynamic payload
    import time
    unique_suffix = int(time.time())
    
    payload = {
        "project_id": project_id,
        "availability_zone_id": az_id, # Дефолтные ID для зоны
        "disk_type_id": disk_type_id,   # и типа диска (обновите в .env при необходимости)
        "name": f"test-disk-{unique_suffix}",
        "description": "Auto-generated test disk",
        "size": 10,
        "readonly": False,
        "shared": False,
        "encrypted": False
    }
    
    request_data = None
    
    # Setup: Create Disk
    with allure.step("1. Attach Request Payload"):
        allure.attach(json.dumps(payload, indent=2), name="Request Payload", attachment_type=allure.attachment_type.JSON)
        
    with allure.step("2. Execute POST /api/v1/disks"):
        response = requests.post(base_url + endpoint, headers=headers, json=payload)
        
    with allure.step("3. Check Status Code 201"):
        if response.status_code != 201:
             pytest.fail(f"Expected 201, got {response.status_code}. Response: {response.text}")
             
    data = response.json()
    
    with allure.step("4. Attach Response Data"):
        allure.attach(json.dumps(data, indent=2), name="Created Disk Response", attachment_type=allure.attachment_type.JSON)
        
    yield data
    
    # Teardown: Delete Disk
    disk_id = data["id"]
    delete_endpoint = f"/api/v1/disks/{disk_id}"
    
    with allure.step(f"Teardown: DELETE /api/v1/disks/{disk_id}"):
        requests.delete(base_url + delete_endpoint, headers=headers)


@allure.feature("DisksCreateAPI")
@allure.story("Story: DisksCreateAPI")
@allure.suite("API")
@allure.link("https://jira.cloud.ru/browse/TASK-API-DISKS-CREATE", name="API Docs")
class TestDisksCreateAPI:
    @allure.title("API Test: Create Disk with Teardown")
    @allure.link("https://jira.cloud.ru/browse/TASK-PENDING", name="Related Task")
    @allure.tag("NORMAL")
    @allure.label("priority", "normal")
    def test_scenario(self, created_disk_data):
        # Validation
        data = created_disk_data
        
        with allure.step("Validate Created Disk Schema"):
            assert "id" in data, "Response missing 'id'"
            assert "name" in data, "Response missing 'name'"
            assert "size" in data, "Response missing 'size'"
            assert "state" in data, "Response missing 'state'"
            assert "created_time" in data, "Response missing 'created_time'"
        
