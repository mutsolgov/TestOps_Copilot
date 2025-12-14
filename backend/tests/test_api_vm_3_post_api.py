import pytest
import allure
import requests
import os
import json
import base64
import time

base_url = "https://compute.api.cloud.ru"
    
@pytest.fixture(scope="function")
def create_vm_and_cleanup():
    base_url = "https://compute.api.cloud.ru"
    endpoint = "/api/v1/vms"
    token = os.getenv("CLOUD_API_TOKEN")
    project_id = os.getenv("TEST_PROJECT_ID")
    ssh_key = os.getenv("TEST_SSH_PUBLIC_KEY")
    
    # Optional with defaults
    az_id = os.getenv("TEST_AZ_ID", "7c99a597-8516-494f-a2c7-d7377048681e")
    flavor_id = os.getenv("TEST_FLAVOR_ID", "139ddd16-2482-4694-991d-9b1834266e03")
    image_id = os.getenv("TEST_IMAGE_ID", "474c9e98-760f-4e54-aaa9-70024814f2b0")
    subnet_id = os.getenv("TEST_SUBNET_ID", "abb61c39-8a65-4735-8d65-55174b795163")
    disk_type_id = os.getenv("TEST_DISK_TYPE_ID", "a859e3dc-6b14-42a8-9bcc-890fde0ba6d0")

    if not all([token, project_id, ssh_key]):
        pytest.skip("Skipping VM test: Missing required env vars (CLOUD_API_TOKEN, TEST_PROJECT_ID, TEST_SSH_PUBLIC_KEY)")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
@pytest.fixture(scope="function")
def create_vm_and_cleanup():
    base_url = "https://compute.api.cloud.ru"
    endpoint = "/api/v1/vms"
    token = os.getenv("CLOUD_API_TOKEN")
    project_id = os.getenv("TEST_PROJECT_ID")
    ssh_key = os.getenv("TEST_SSH_PUBLIC_KEY")
    
    # Optional with defaults
    az_id = os.getenv("TEST_AZ_ID", "7c99a597-8516-494f-a2c7-d7377048681e")
    flavor_id = os.getenv("TEST_FLAVOR_ID", "139ddd16-2482-4694-991d-9b1834266e03")
    image_id = os.getenv("TEST_IMAGE_ID", "474c9e98-760f-4e54-aaa9-70024814f2b0")
    subnet_id = os.getenv("TEST_SUBNET_ID", "abb61c39-8a65-4735-8d65-55174b795163")
    disk_type_id = os.getenv("TEST_DISK_TYPE_ID", "a859e3dc-6b14-42a8-9bcc-890fde0ba6d0")

    if not all([token, project_id, ssh_key]):
        pytest.skip("Skipping VM test: Missing required env vars (CLOUD_API_TOKEN, TEST_PROJECT_ID, TEST_SSH_PUBLIC_KEY)")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    import time
    import base64
    unique_suffix = int(time.time())
    vm_name = f"test-vm-{unique_suffix}"
    disk_name = f"root-disk-{unique_suffix}"
    
    # 2. Prepare Cloud-init with embedded SSH key
    cloud_init_raw = f'''
#cloud-config
users:
  - name: ubuntu
    ssh-authorized-keys:
      - {ssh_key}
    sudo: ALL
'''
    cloud_init_b64 = base64.b64encode(cloud_init_raw.encode("utf-8")).decode("utf-8")
    
    payload = [
      {
        "project_id": project_id,
        "name": vm_name,
        "flavor_id": flavor_id,
        "image_id": image_id,
        "availability_zone_id": az_id, # AZ at root level
        "disks": [
            {
                "name": disk_name, # Correct field name
                "disk_type_id": disk_type_id,
                "size": 10
            }
        ],
        "subnets": [
            {
                "subnet_id": subnet_id
            }
        ],
        "description": "Auto-generated test VM",
        "cloud_init": cloud_init_b64 # Cloud-init at root level, Base64
      }
    ]

    request_body = json.dumps(payload, indent=2)
    with allure.step("1. Attach VM Payload"):
        allure.attach(request_body, name="VM Request Body", attachment_type=allure.attachment_type.JSON)

    with allure.step(f"2. Execute POST {endpoint}"):
        response = requests.post(base_url + endpoint, headers=headers, json=payload)
        
    with allure.step("3. Check Status Code 201"):
        if response.status_code != 201:
             pytest.fail(f"Expected 201, got {response.status_code}. Response: {response.text}")
    
    data = response.json()
    created_vm_id = data[0]["id"]
    
    yield created_vm_id
    
    # Teardown
    delete_endpoint = f"/api/v1/vms/{created_vm_id}"
    with allure.step(f"Teardown: DELETE {delete_endpoint}"):
        # Attempt minimal stop before delete just in case
        try:
             shutdown_payload = [{ "id": created_vm_id, "state": "stopped" }]
             requests.put(base_url + endpoint, headers=headers, json=shutdown_payload)
             time.sleep(1)
        except:
             pass
        requests.delete(base_url + delete_endpoint, headers=headers)


@allure.feature("VMCreationAPI")
@allure.story("Story: VMCreationAPI")
@allure.suite("API")
@allure.link("https://jira.cloud.ru/browse/TASK-API-VM-CREATE", name="API Docs")
class TestVMCreationAPI:
    @allure.title("API Test: Create VM with Lifecycle")
    @allure.link("https://jira.cloud.ru/browse/TASK-PENDING", name="Related Task")
    @allure.tag("NORMAL")
    @allure.label("priority", "normal")
    def test_scenario(self, create_vm_and_cleanup):
        # Validation
        vm_id = create_vm_and_cleanup
        
        with allure.step("Validate VM Created"):
            assert vm_id, "VM ID should not be empty"
            
        endpoint = f"/api/v1/vms/{vm_id}"
        headers = {
            "Authorization": f"Bearer {os.getenv('CLOUD_API_TOKEN')}",
            "Content-Type": "application/json"
        }
        
        # Verify VM details
        with allure.step(f"GET {endpoint}"):
            response = requests.get(base_url + endpoint, headers=headers)
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            data = response.json()
            assert data["id"] == vm_id
            assert "state" in data
            assert "name" in data
        

