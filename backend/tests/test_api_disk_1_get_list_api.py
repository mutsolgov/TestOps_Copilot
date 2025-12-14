import pytest
import allure
import requests
import os
import json


@pytest.fixture(scope="function")
def disk_list_data():
    project_id = os.getenv("TEST_PROJECT_ID")
    token = os.getenv("CLOUD_API_TOKEN")
    base_url = "https://compute.api.cloud.ru"
    endpoint = "/api/v1/disks"
    
    assert project_id, "Please set TEST_PROJECT_ID in your .env file"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    params = {
        "project_id": project_id,
        "limit": 10,
        "order_by": "created_time",
        "order_desc": "true"
    }
    
    with allure.step("1. Execute API GET /api/v1/disks"):
        response = requests.get(base_url + endpoint, headers=headers, params=params)
        
    with allure.step("2. Check Status Code 200"):
        if response.status_code != 200:
            pytest.fail(f"Expected 200, got {response.status_code}")

    with allure.step("3. Attach Full Response JSON"):
        allure.attach(json.dumps(response.json(), indent=2), name="Disks List Full JSON Response", attachment_type=allure.attachment_type.JSON)
        
    return response.json()


@allure.feature("DisksListAPI")
@allure.story("Story: DisksListAPI")
@allure.suite("API")
@allure.link("https://jira.cloud.ru/browse/TASK-API-DISKS-LIST", name="API Docs")
class TestDisksListAPI:
    @allure.title("API Test: Get Disks List")
    @allure.link("https://jira.cloud.ru/browse/TASK-PENDING", name="Related Task")
    @allure.tag("NORMAL")
    @allure.label("priority", "normal")
    def test_scenario(self, disk_list_data):
        # Validation
        data = disk_list_data
        
        with allure.step("Validate Response Schema"):
            assert "items" in data, "Response missing 'items' field"
            assert isinstance(data["items"], list), "'items' must be a list"
            assert "total" in data, "Response missing 'total' field"
            
        with allure.step("Validate Disk Item Structure"):
            if data["items"]:
                disk = data["items"][0]
                assert "id" in disk, "Disk missing 'id'"
                assert "name" in disk, "Disk missing 'name'"
                assert "size" in disk, "Disk missing 'size'"
                assert "state" in disk, "Disk missing 'state'"
                assert "disk_type" in disk, "Disk missing 'disk_type'"
        

