import pytest
import allure
import requests
import os
import time # Добавляем импорт для уникальности
import base64

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
        token = os.getenv("CLOUD_API_TOKEN")

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # --- ИСПРАВЛЕНИЯ: Подготовка данных с правильными отступами ---
        
        # 1. Уникальные имена (для избежания 409 Conflict)
        unique_suffix = int(time.time())
        VM_NAME = f"test-vm-{unique_suffix}"
        DISK_NAME = f"root-disk-{unique_suffix}"
        
        # 2. Подготовка Cloud-init (Исправление IndentationError)
        ssh_key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIBJ6i+hm43CEcEIuw0onvehbYW0rbcIHJnRGpVQqS1NX muhammad@222"
        cloud_init_script = f"""
#cloud-config
users:
  - name: ubuntu
    ssh-authorized-keys:
      - {ssh_key}
    sudo: ALL
"""
        # -------------------------------------------------------------------
        bytes_script = cloud_init_script.encode("utf-8")
        # 2. Затем кодируем байты в Base64
        base64_encoded_script = base64.b64encode(bytes_script)
        # 3. Декодируем байты Base64 в строку, чтобы передать в JSON
        cloud_init_final = base64_encoded_script.decode("utf-8")
        
        # Payload: Array of objects (as per docs)
        payload = [
          {
            "project_id": "4582273a-e0e7-4fb4-b284-8a91cb03d106",
            "name": VM_NAME, # <<< ИСПРАВЛЕНО: Уникальное имя
            "availability_zone_id": "7c99a597-8516-494f-a2c7-d7377048681e", # <<< ДОБАВЛЕНО: AZ на корневом уровне
            "flavor_id": "139ddd16-2482-4694-991d-9b1834266e03",
            "image_id": "474c9e98-760f-4e54-aaa9-70024814f2b0",
            
            "subnets": [
                {
                "subnet_id": "abb61c39-8a65-4735-8d65-55174b795163"
                }
            ],
            "disks": [
                {
                "name": DISK_NAME, # <<< ИСПРАВЛЕНО: Уникальное имя диска
                "size": 10,
                "disk_type_id": "a859e3dc-6b14-42a8-9bcc-890fde0ba6d0",
                #"availability_zone_id": "7c99a597-8516-494f-a2c7-d7377048681e"
                }
            ],
            
            "description": "Auto-generated test VM",
            "cloud_init": cloud_init_final
          }
        ]

        # Act
        with allure.step(f"POST {endpoint}"):
            response = requests.post(base_url + endpoint, headers=headers, json=payload)

        # Assert
        with allure.step("Check Status Code 201 (Created)"):
            assert response.status_code == 201, f"Expected 201, got {response.status_code}. Response: {response.text}"
        
        data = response.json()
        
        with allure.step("Validate Response Schema"):
            assert isinstance(data, list), "Response should be a list"
            if data:
                vm = data[0]
                assert "id" in vm, "Missing 'id'"
                assert "state" in vm, "Missing 'state'"
