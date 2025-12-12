from abc import ABC, abstractmethod
from app.core.config import settings

class AIProvider(ABC):
    @abstractmethod
    async def generate_test_case(self, prompt: str) -> str:
        pass

    def _clean_code(self, code: str) -> str:
        code = code.strip()
        if code.startswith("```python"):
            code = code[9:]
        elif code.startswith("```"):
            code = code[3:]
        if code.endswith("```"):
            code = code[:-3]
        return code.strip()

class MockAIProvider(AIProvider):
    async def generate_test_case(self, prompt: str) -> str:
        feature_name = "GeneratedTest"
        raw_reqs = ""
        owner = "qa_user"
        priority = "normal"
        test_type = "UI"

        try:
            if "Owner:" in prompt:
                owner = prompt.split("Owner:")[1].split("\n")[0].strip()
            if "Priority:" in prompt:
                priority = prompt.split("Priority:")[1].split("\n")[0].strip()
            if "Test Type:" in prompt:
                parsed_type = prompt.split("Test Type:")[1].split("\n")[0].strip()
                if "API" in parsed_type or "Backend" in parsed_type:
                    test_type = "API"
                else:
                    test_type = "UI"
        except:
            pass
        
        if "User Requirements:" in prompt:
            try:
                raw_reqs = prompt.split("User Requirements:")[1].split("Owner:")[0].strip()
                words = [w for w in raw_reqs.split() if w.isalnum()]
                if words:
                    feature_name = "".join(words[:4]).capitalize()
            except:
                pass

        normalized_steps = []
        if raw_reqs:
            raw_lines = [l.strip() for l in raw_reqs.split('\n') if l.strip()]
            current_step = ""
            for line in raw_lines:
                is_bullet = line.startswith(('-', '*', '•')) or (line[0].isdigit() and line[1] == '.')
                if is_bullet:
                    if current_step: normalized_steps.append(current_step)
                    current_step = line.lstrip("-*•1234567890. ")
                else:
                    if current_step:
                        if current_step.endswith("-"): current_step = current_step[:-1] + line
                        else: current_step += " " + line
                    else:
                        current_step = line
            if current_step: normalized_steps.append(current_step)

        req_text_lower = raw_reqs.lower().replace("\n", " ").replace("  ", " ") if raw_reqs else ""
        context = "MAIN"
        start_step_title = "Открыть главную страницу сервиса"
        feature_name = "GenericFeature"

        if any(x in req_text_lower for x in ["api/v1/vms", "список виртуальных машин", "get vm list", "получение списка виртуальных машин"]):
            context = "API_VMS"
            feature_name = "VirtualMachinesAPI"
            test_type = "API" 
        elif any(x in req_text_lower for x in ["изменение статуса виртуальной машины", "change vm status", "put ", "put "]):
            context = "API_VM_STATUS"
            feature_name = "VMStatusManagement"
            test_type = "API"
        elif any(x in req_text_lower for x in ["создание виртуальной машины", "create vm", "post ", "post "]):
            context = "API_VM_CREATE"
            feature_name = "VMCreationAPI"
            test_type = "API"
        elif any(x in req_text_lower for x in ["получение информации о виртуальной машине", "get vm details"]):
            context = "API_VM_DETAILS"
            feature_name = "VMDetailsAPI"
            test_type = "API"
        elif any(x in req_text_lower for x in ["обновление виртуальной машины", "update vm"]):
            context = "API_VM_UPDATE"
            feature_name = "VMUpdateAPI"
            test_type = "API"
        elif any(x in req_text_lower for x in ["удаление виртуальной машины", "delete vm"]):
            context = "API_VM_DELETE"
            feature_name = "VMDeletionAPI"
            test_type = "API"
        elif any(x in req_text_lower for x in ["получение списка дисков", "get disk list"]):
            context = "API_DISKS_LIST"
            feature_name = "DisksListAPI"
            test_type = "API"
        elif any(x in req_text_lower for x in ["создание диска", "create disk"]):
            context = "API_DISKS_CREATE"
            feature_name = "DisksCreateAPI"
            test_type = "API"
        elif any(x in req_text_lower for x in ["получение информации о диске", "get disk details"]):
            context = "API_DISK_DETAILS"
            feature_name = "DiskDetailsAPI"
            test_type = "API"
        elif any(x in req_text_lower for x in ["обновление диска", "update disk"]):
            context = "API_DISK_UPDATE"
            feature_name = "DiskUpdateAPI"
            test_type = "API"
        elif any(x in req_text_lower for x in ["удаление диска", "delete disk"]):
            context = "API_DISK_DELETE"
            feature_name = "DiskDeleteAPI"
            test_type = "API"
        elif any(x in req_text_lower for x in ["подключение диска", "attach disk"]):
            context = "API_DISK_ATTACH"
            feature_name = "DiskAttachAPI"
            test_type = "API"
        elif any(x in req_text_lower for x in ["отключение диска", "detach disk"]):
            context = "API_DISK_DETACH"
            feature_name = "DiskDetachAPI"
            test_type = "API"
        elif any(token in req_text_lower for token in ["флейвор", "flavor"]) and \
             any(action in req_text_lower for action in ["список", "list", "get all", "получить все"]):
            context = "API_FLAVORS_LIST"
            feature_name = "FlavorsListAPI"
            test_type = "API"
        elif any(token in req_text_lower for token in ["флейвор", "flavor"]) and \
             any(action in req_text_lower for action in ["информаци", "details", "получение", "получить"]):
            context = "API_FLAVORS_DETAILS"
            feature_name = "FlavorsDetailsAPI"
            test_type = "API"
        elif any(x in req_text_lower for x in ["главная страница", "начальная страница"]):
            context = "MAIN"
            start_step_title = "Открыть главную страницу сервиса"
            feature_name = "PriceCalculatorUI"
        elif any(x in req_text_lower for x in ["мобильн", "mobile", "адаптив"]):
            context = "MOBILE"
            start_step_title = "Открыть сервис на мобильном устройстве"
            feature_name = "MobileResponsiveness"
        elif any(x in req_text_lower for x in ["управление", "сравнение", "удаление сервиса"]):
            context = "MANAGEMENT"
            start_step_title = "Перейти к управлению конфигурацией"
            feature_name = "ConfigurationManagement"
        elif any(x in req_text_lower for x in ["категор", "каталог", "фильтр", "поиск"]):
            context = "CATALOG"
            start_step_title = "Перейти в раздел 'Каталог продуктов'"
            feature_name = "ProductCatalog"
        elif any(x in req_text_lower for x in ["конфигурац", "параметр", "диапазон"]):
            context = "CONFIG"
            start_step_title = "Выбрать продукт и перейти на экран конфигурации"
            feature_name = "ProductConfiguration"
        
        api_imports = "import pytest\nimport allure\nimport requests\nimport os"

        if test_type == "API" and context == "API_VMS":
             code_body = f"""        # Arrange
        base_url = "https://compute.api.cloud.ru"
        endpoint = "/api/v1/vms"
        
        # Configuration
        project_id = os.getenv("TEST_PROJECT_ID")
        token = os.getenv("CLOUD_API_TOKEN") # Security fix
        
        # Validation
        assert project_id, "Please set TEST_PROJECT_ID in your .env file"
        
        headers = {{
            "Authorization": f"Bearer {{token}}",
            "Content-Type": "application/json"
        }}
        params = {{
            "project_id": project_id,
            "limit": 50
        }}

        # Act
        with allure.step(f"GET {{endpoint}}"):
            response = requests.get(base_url + endpoint, headers=headers, params=params)

        # Assert
        with allure.step("Check Status Code 200"):
            assert response.status_code == 200, f"Expected 200, got {{response.status_code}}"
        
        data = response.json()
        
        with allure.step("Validate Response Schema"):
            assert "items" in data, "Response missing 'items' field"
            assert "total" in data, "Response missing 'total' field"
            assert isinstance(data["items"], list), "'items' must be a list"
            
        with allure.step("Validate Item Structure"):
            if data["items"]:
                item = data["items"][0]
                assert "id" in item
                assert "name" in item
                assert "state" in item"""
             
             decorators = f"""@allure.feature("{feature_name}")
@allure.story("Story: {feature_name}")
@allure.suite("API")
@allure.link("https://jira.cloud.ru/browse/TASK-API-VMS", name="API Docs")"""

             return f"""{api_imports}

{decorators}
class Test{feature_name}:
    @allure.title("API Test: Get VM List")
    @allure.link("https://jira.cloud.ru/browse/TASK-PENDING", name="Related Task")
    @allure.tag("{priority.upper()}")
    @allure.label("priority", "{priority.lower()}")
    def test_scenario(self):
{code_body}
"""

        if test_type == "API" and context == "API_VM_STATUS":
             code_body = f"""        # Arrange
        base_url = "https://compute.api.cloud.ru"
        
        # Configuration
        vm_id = os.getenv("TEST_VM_ID")
        token = os.getenv("CLOUD_API_TOKEN") # Security fix
        
        # Validation
        assert vm_id, "Please set TEST_VM_ID in your .env file"

        vm_endpoint = f"/api/v1/vms/{{vm_id}}"
        bulk_endpoint = "/api/v1/vms"
        
        headers = {{
            "Authorization": f"Bearer {{token}}",
            "Content-Type": "application/json"
        }}
        
        # Step 1: Get Current State
        with allure.step(f"GET {{vm_endpoint}}"):
            response_get = requests.get(base_url + vm_endpoint, headers=headers)
            assert response_get.status_code == 200, "Failed to get current VM info"
            current_state = response_get.json()["state"]
            
        # Step 2: Determine Target State
        target_state = "stopped" if current_state == "running" else "running"

        # Step 3: PUT New State (Bulk Endpoint)
        payload = [
          {{
            "id": vm_id,
            "state": target_state
          }}
        ]

        # Act
        with allure.step(f"PUT {{bulk_endpoint}} -> Switch to {{target_state}}"):
            response = requests.put(base_url + bulk_endpoint, headers=headers, json=payload)

        # Assert
        with allure.step("Check Status Code 204"):
            assert response.status_code == 204, f"Expected 204, got {{response.status_code}}"
        """
             
             decorators = f"""@allure.feature("{feature_name}")
@allure.story("Story: {feature_name}")
@allure.suite("API")
@allure.link("https://jira.cloud.ru/browse/TASK-API-VM-STATUS", name="API Docs")"""

             return f"""{api_imports}

{decorators}
class Test{feature_name}:
    @allure.title("API Test: Change VM Status")
    @allure.link("https://jira.cloud.ru/browse/TASK-PENDING", name="Related Task")
    @allure.tag("{priority.upper()}")
    @allure.label("priority", "{priority.lower()}")
    def test_scenario(self):
{code_body}
"""

        if test_type == "API" and context == "API_VM_CREATE":
             code_body = f"""        # Arrange
        base_url = "https://compute.api.cloud.ru"
        endpoint = "/api/v1/vms"
        token = os.getenv("CLOUD_API_TOKEN") # Security fix
        
        headers = {{
            "Authorization": f"Bearer {{token}}",
            "Content-Type": "application/json"
        }}
        
        # Payload: Array of objects (as per docs)
        payload = [
          {{
            "project_id": "405d8375-3514-403b-8c43-83ae74cfe0e9",
            "name": "test-vm-01",
            "flavor_id": "fa3e89aa-6829-47f5-8bf4-76d57211a9f1",
            "image_id": "84c230fd-5520-4984-8119-37365b66fd80",
            # Required array fields
            "disks": [
                {{
                    "disk_id": "9fb32f13-bddc-42b3-9a07-4aed1801aae6",
                    "disk_name": "boot-disk"
                }}
            ],
            # Optional fields populated from sample
            "description": "Auto-generated test VM",
            "cloud_init": "#!/bin/bash\\necho hello"
          }}
        ]

        # Act
        with allure.step(f"POST {{endpoint}}"):
            response = requests.post(base_url + endpoint, headers=headers, json=payload)

        # Assert
        with allure.step("Check Status Code 201 (Created)"):
            assert response.status_code == 201, f"Expected 201, got {{response.status_code}}"
        
        data = response.json()
        
        with allure.step("Validate Response Schema"):
            # Check for Array response (as per docs: Response Code 201 -> Array)
            assert isinstance(data, list), "Response should be a list"
            if data:
                vm = data[0]
                assert "id" in vm, "Missing 'id'"
                assert "state" in vm, "Missing 'state'"
        """
             
             decorators = f"""@allure.feature("{feature_name}")
@allure.story("Story: {feature_name}")
@allure.suite("API")
@allure.link("https://jira.cloud.ru/browse/TASK-API-VM-CREATE", name="API Docs")"""

             return f"""{api_imports}

{decorators}
class Test{feature_name}:
    @allure.title("API Test: Create VM")
    @allure.link("https://jira.cloud.ru/browse/TASK-PENDING", name="Related Task")
    @allure.tag("{priority.upper()}")
    @allure.label("priority", "{priority.lower()}")
    def test_scenario(self):
{code_body}
"""

        if test_type == "API" and context == "API_VM_DETAILS":
             code_body = f"""        # Arrange
        base_url = "https://compute.api.cloud.ru"
        
        # Configuration
        vm_id = os.getenv("TEST_VM_ID")
        
        # Validation
        assert vm_id, "Please set TEST_VM_ID in your .env file"

        endpoint = f"/api/v1/vms/{{vm_id}}"
        token = os.getenv("CLOUD_API_TOKEN") # Security fix
        
        headers = {{
            "Authorization": f"Bearer {{token}}",
            "Content-Type": "application/json"
        }}

        # Act
        with allure.step(f"GET {{endpoint}}"):
            response = requests.get(base_url + endpoint, headers=headers)

        # Assert
        with allure.step("Check Status Code 200"):
            assert response.status_code == 200, f"Expected 200, got {{response.status_code}}"
        
        data = response.json()
        
        with allure.step("Validate Response Structure (Object)"):
            assert isinstance(data, dict), "Response should be a JSON Object"
            assert "id" in data
            assert "name" in data
            assert "state" in data
            assert "flavor" in data
            assert "interfaces" in data
        
        with allure.step("Validate Nested Objects"):
             if "flavor" in data:
                 assert "id" in data["flavor"]
                 assert "cpu" in data["flavor"]
        """
             
             decorators = f"""@allure.feature("{feature_name}")
@allure.story("Story: {feature_name}")
@allure.suite("API")
@allure.link("https://jira.cloud.ru/browse/TASK-API-VM-DETAILS", name="API Docs")"""

             return f"""{api_imports}

{decorators}
class Test{feature_name}:
    @allure.title("API Test: Get VM Details")
    @allure.link("https://jira.cloud.ru/browse/TASK-PENDING", name="Related Task")
    @allure.tag("{priority.upper()}")
    @allure.label("priority", "{priority.lower()}")
    def test_scenario(self):
{code_body}
"""

        if test_type == "API" and context == "API_VM_UPDATE":
             code_body = f"""        # Arrange
        base_url = "https://compute.api.cloud.ru"
        
        # Configuration
        vm_id = os.getenv("TEST_VM_ID")
        
        # Validation
        assert vm_id, "Please set TEST_VM_ID in your .env file"
        
        endpoint = f"/api/v1/vms/{{vm_id}}"
        token = os.getenv("CLOUD_API_TOKEN") # Security fix
        
        headers = {{
            "Authorization": f"Bearer {{token}}",
            "Content-Type": "application/json"
        }}
        
        payload = {{
            "name": "Updated Name",
            "description": "Updated Description",
            "flavor_id": "fa3e89aa-6829-47f5-8bf4-76d57211a9f1"
        }}

        # Act
        with allure.step(f"PUT {{endpoint}}"):
            response = requests.put(base_url + endpoint, headers=headers, json=payload)

        # Assert
        with allure.step("Check Status Code 200"):
            assert response.status_code == 200, f"Expected 200, got {{response.status_code}}"
        
        data = response.json()
        
        with allure.step("Validate Response Structure"):
            assert isinstance(data, dict), "Response should be a JSON Object"
            assert data["id"] == vm_id, "ID should match"
            assert "name" in data
        """
             
             decorators = f"""@allure.feature("{feature_name}")
@allure.story("Story: {feature_name}")
@allure.suite("API")
@allure.link("https://jira.cloud.ru/browse/TASK-API-VM-UPDATE", name="API Docs")"""

             return f"""{api_imports}

{decorators}
class Test{feature_name}:
    @allure.title("API Test: Update VM")
    @allure.link("https://jira.cloud.ru/browse/TASK-PENDING", name="Related Task")
    @allure.tag("{priority.upper()}")
    @allure.label("priority", "{priority.lower()}")
    def test_scenario(self):
{code_body}
"""

        if test_type == "API" and context == "API_VM_DELETE":
             code_body = f"""        # Arrange
        base_url = "https://compute.api.cloud.ru"
        
        # Configuration
        vm_id = os.getenv("TEST_VM_ID")
        disk_id = os.getenv("TEST_DISK_VM_ID")
        external_ips = os.getenv("TEST_EXTERNAL_IPS") # если ip нет оставьте просто []
        token = os.getenv("CLOUD_API_TOKEN")
        
        # Validation
        error_msg = "Please set TEST_VM_ID, TEST_DISK_VM_ID and TEST_EXTERNAL_IPS in your .env file"
        assert vm_id, error_msg
        assert disk_id, error_msg
        assert external_ips is not None, error_msg

        endpoint = f"/api/v1/vms/{{vm_id}}"
        
        headers = {{
            "Authorization": f"Bearer {{token}}",
            "Content-Type": "application/json"
        }}
        
        # Process external_ips string to list
        ips_list = [ip.strip() for ip in external_ips.split(',')] if external_ips else []
        
        payload = {{
          "delete_attachments": {{
            "disk_ids": [disk_id],
            "external_ips": ips_list
          }}
        }}

        # Act
        with allure.step(f"DELETE {{endpoint}}"):
            response = requests.request("DELETE", base_url + endpoint, headers=headers, json=payload)

        # Assert
        with allure.step("Check Status Code 204"):
            assert response.status_code == 204, f"Expected 204, got {{response.status_code}}"
        """
             
             decorators = f"""@allure.feature("{feature_name}")
@allure.story("Story: {feature_name}")
@allure.suite("API")
@allure.link("https://jira.cloud.ru/browse/TASK-API-VM-DELETE", name="API Docs")"""

             return f"""{api_imports}

{decorators}
class Test{feature_name}:
    @allure.title("API Test: Delete VM")
    @allure.link("https://jira.cloud.ru/browse/TASK-PENDING", name="Related Task")
    @allure.tag("{priority.upper()}")
    @allure.label("priority", "{priority.lower()}")
    def test_scenario(self):
{code_body}
"""
        if test_type == "API" and context == "API_DISKS_LIST":
             code_body = f"""        # Arrange
        base_url = "https://compute.api.cloud.ru"
        endpoint = "/api/v1/disks"
        
        # Configuration
        project_id = os.getenv("TEST_PROJECT_ID")
        token = os.getenv("CLOUD_API_TOKEN")
        
        # Validation
        assert project_id, "Please set TEST_PROJECT_ID in your .env file"
        
        headers = {{
            "Authorization": f"Bearer {{token}}",
            "Content-Type": "application/json"
        }}
        
        params = {{
            "project_id": project_id,
            "limit": 10,
            "order_by": "created_time",
            "order_desc": "true"
        }}

        # Act
        with allure.step(f"GET {{endpoint}}"):
            response = requests.get(base_url + endpoint, headers=headers, params=params)

        # Assert
        with allure.step("Check Status Code 200"):
            assert response.status_code == 200, f"Expected 200, got {{response.status_code}}"
        
        data = response.json()
        
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
        """
             
             decorators = f"""@allure.feature("{feature_name}")
@allure.story("Story: {feature_name}")
@allure.suite("API")
@allure.link("https://jira.cloud.ru/browse/TASK-API-DISKS-LIST", name="API Docs")"""

             return f"""{api_imports}

{decorators}
class Test{feature_name}:
    @allure.title("API Test: Get Disks List")
    @allure.link("https://jira.cloud.ru/browse/TASK-PENDING", name="Related Task")
    @allure.tag("{priority.upper()}")
    @allure.label("priority", "{priority.lower()}")
    def test_scenario(self):
{code_body}
"""

        if test_type == "API" and context == "API_DISKS_CREATE":
             code_body = f"""        # Arrange
        base_url = "https://compute.api.cloud.ru"
        endpoint = "/api/v1/disks"
        
        # Configuration
        project_id = os.getenv("TEST_PROJECT_ID")
        token = os.getenv("CLOUD_API_TOKEN")
        
        # Validation
        assert project_id, "Please set TEST_PROJECT_ID in your .env file"
        
        headers = {{
            "Authorization": f"Bearer {{token}}",
            "Content-Type": "application/json"
        }}
        
        # Dynamic payload with unique name to avoid 409
        import time
        unique_suffix = int(time.time())
        
        payload = {{
            "project_id": project_id,
            "availability_zone_id": "00000000-0000-0000-0000-000000000000", # Example ID, replace if needed
            "disk_type_id": "00000000-0000-0000-0000-000000000000", # Example ID, replace if needed
            "name": f"test-disk-{{unique_suffix}}",
            "description": "Auto-generated test disk",
            "size": 10,
            "readonly": False,
            "shared": False,
            "encrypted": False
        }}

        # Act
        with allure.step(f"POST {{endpoint}}"):
            response = requests.post(base_url + endpoint, headers=headers, json=payload)

        # Assert
        with allure.step("Check Status Code 201"):
            assert response.status_code == 201, f"Expected 201, got {{response.status_code}}"
        
        data = response.json()
        
        with allure.step("Validate Response Schema"):
            assert "id" in data, "Response missing 'id'"
            assert data["name"] == payload["name"], "Name mismatch"
            assert data["size"] == payload["size"], "Size mismatch"
            assert "state" in data, "Response missing 'state'"
            assert "created_time" in data, "Response missing 'created_time'"
        """
             
             decorators = f"""@allure.feature("{feature_name}")
@allure.story("Story: {feature_name}")
@allure.suite("API")
@allure.link("https://jira.cloud.ru/browse/TASK-API-DISKS-CREATE", name="API Docs")"""

             return f"""{api_imports}

{decorators}
class Test{feature_name}:
    @allure.title("API Test: Create Disk")
    @allure.link("https://jira.cloud.ru/browse/TASK-PENDING", name="Related Task")
    @allure.tag("{priority.upper()}")
    @allure.label("priority", "{priority.lower()}")
    def test_scenario(self):
{code_body}
"""

        if test_type == "API" and context == "API_DISK_DETAILS":
             code_body = f"""        # Arrange
        base_url = "https://compute.api.cloud.ru"
        
        # Configuration
        disk_id = os.getenv("TEST_DISK_ID")
        token = os.getenv("CLOUD_API_TOKEN")
        
        # Validation
        assert disk_id, "Please set TEST_DISK_ID in your .env file"
        
        endpoint = f"/api/v1/disks/{{disk_id}}"
        
        headers = {{
            "Authorization": f"Bearer {{token}}",
            "Content-Type": "application/json"
        }}

        # Act
        with allure.step(f"GET {{endpoint}}"):
            response = requests.get(base_url + endpoint, headers=headers)

        # Assert
        with allure.step("Check Status Code 200"):
            assert response.status_code == 200, f"Expected 200, got {{response.status_code}}"
        
        data = response.json()
        
        with allure.step("Validate Response Schema"):
            assert "id" in data, "Response missing 'id'"
            assert data["id"] == disk_id, "ID mismatch"
            assert "name" in data, "Response missing 'name'"
            assert "size" in data, "Response missing 'size'"
            assert "state" in data, "Response missing 'state'"
            assert "created_time" in data, "Response missing 'created_time'"
            
        with allure.step("Validate Nested Objects"):
            assert "disk_type" in data, "Response missing 'disk_type'"
            assert "availability_zone" in data, "Response missing 'availability_zone'"
        """
             
             decorators = f"""@allure.feature("{feature_name}")
@allure.story("Story: {feature_name}")
@allure.suite("API")
@allure.link("https://jira.cloud.ru/browse/TASK-API-DISK-DETAILS", name="API Docs")"""

             return f"""{api_imports}

{decorators}
class Test{feature_name}:
    @allure.title("API Test: Get Disk Details")
    @allure.link("https://jira.cloud.ru/browse/TASK-PENDING", name="Related Task")
    @allure.tag("{priority.upper()}")
    @allure.label("priority", "{priority.lower()}")
    def test_scenario(self):
{code_body}
"""
        
        if test_type == "API" and context == "API_DISK_UPDATE":
             code_body = f"""        # Arrange
        base_url = "https://compute.api.cloud.ru"
        
        # Configuration
        disk_id = os.getenv("TEST_DISK_ID")
        token = os.getenv("CLOUD_API_TOKEN")
        
        # Validation
        assert disk_id, "Please set TEST_DISK_ID in your .env file"
        
        endpoint = f"/api/v1/disks/{{disk_id}}"
        
        headers = {{
            "Authorization": f"Bearer {{token}}",
            "Content-Type": "application/json"
        }}
        
        # Dynamic Payload
        import time
        unique_suffix = int(time.time())
        payload = {{
            "name": f"updated-disk-{{unique_suffix}}",
            "description": "Updated description",
            "size": 10, # Size must be >= current size, assume 10 is safe or equal
            "readonly": False,
            "shared": False,
            "encrypted": False
        }}

        # Act
        with allure.step(f"PUT {{endpoint}}"):
            response = requests.put(base_url + endpoint, headers=headers, json=payload)

        # Assert
        with allure.step("Check Status Code 200"):
            assert response.status_code == 200, f"Expected 200, got {{response.status_code}}"
        
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
        """
             
             decorators = f"""@allure.feature("{feature_name}")
@allure.story("Story: {feature_name}")
@allure.suite("API")
@allure.link("https://jira.cloud.ru/browse/TASK-API-DISK-UPDATE", name="API Docs")"""

             return f"""{api_imports}

{decorators}
class Test{feature_name}:
    @allure.title("API Test: Update Disk")
    @allure.link("https://jira.cloud.ru/browse/TASK-PENDING", name="Related Task")
    @allure.tag("{priority.upper()}")
    @allure.label("priority", "{priority.lower()}")
    def test_scenario(self):
{code_body}
"""

        if test_type == "API" and context == "API_DISK_DELETE":
             code_body = f"""        # Arrange
        base_url = "https://compute.api.cloud.ru"
        
        # Configuration
        disk_id = os.getenv("TEST_DISK_ID")
        token = os.getenv("CLOUD_API_TOKEN")
        
        # Validation
        assert disk_id, "Please set TEST_DISK_ID in your .env file"
        
        endpoint = f"/api/v1/disks/{{disk_id}}"
        
        headers = {{
            "Authorization": f"Bearer {{token}}",
        }}

        # Act
        with allure.step(f"DELETE {{endpoint}}"):
            response = requests.delete(base_url + endpoint, headers=headers)

        # Assert
        with allure.step("Check Status Code 204"):
            assert response.status_code == 204, f"Expected 204, got {{response.status_code}}"
        """
             
             decorators = f"""@allure.feature("{feature_name}")
@allure.story("Story: {feature_name}")
@allure.suite("API")
@allure.link("https://jira.cloud.ru/browse/TASK-API-DISK-DELETE", name="API Docs")"""

             return f"""{api_imports}

{decorators}
class Test{feature_name}:
    @allure.title("API Test: Delete Disk")
    @allure.link("https://jira.cloud.ru/browse/TASK-PENDING", name="Related Task")
    @allure.tag("{priority.upper()}")
    @allure.label("priority", "{priority.lower()}")
    def test_scenario(self):
{code_body}
"""

        if test_type == "API" and context == "API_DISK_ATTACH":
             code_body = f"""        # Arrange
        base_url = "https://compute.api.cloud.ru"
        
        # Configuration
        disk_id = os.getenv("TEST_DISK_ID")
        vm_id = os.getenv("TEST_VM_ID")
        token = os.getenv("CLOUD_API_TOKEN")
        
        # Validation
        error_msg = "Please set TEST_DISK_ID and TEST_VM_ID in your .env file"
        assert disk_id, error_msg
        assert vm_id, error_msg
        
        endpoint = f"/api/v1/disks/{{disk_id}}/attach"
        
        headers = {{
            "Authorization": f"Bearer {{token}}",
            "Content-Type": "application/json"
        }}
        
        payload = {{
            "vm_id": vm_id
        }}

        # Act
        with allure.step(f"POST {{endpoint}}"):
            response = requests.post(base_url + endpoint, headers=headers, json=payload)

        # Assert
        with allure.step("Check Status Code 200"):
            assert response.status_code == 200, f"Expected 200, got {{response.status_code}}"
        
        data = response.json()
        
        with allure.step("Validate Response Schema"):
            assert "id" in data, "Response missing 'id'"
            assert data["id"] == disk_id, "ID mismatch"
            assert "vms" in data, "Response missing 'vms' list"
            assert isinstance(data["vms"], list), "'vms' must be a list"
            
        with allure.step("Validate Attachment"):
            # Check if the VM we attached to is in the 'vms' list
            attached_vm_ids = [vm["id"] for vm in data["vms"]]
            assert vm_id in attached_vm_ids, f"VM {{vm_id}} not found in disk attachments"
        """
             
             decorators = f"""@allure.feature("{feature_name}")
@allure.story("Story: {feature_name}")
@allure.suite("API")
@allure.link("https://jira.cloud.ru/browse/TASK-API-DISK-ATTACH", name="API Docs")"""

             return f"""{api_imports}

{decorators}
class Test{feature_name}:
    @allure.title("API Test: Attach Disk to VM")
    @allure.link("https://jira.cloud.ru/browse/TASK-PENDING", name="Related Task")
    @allure.tag("{priority.upper()}")
    @allure.label("priority", "{priority.lower()}")
    def test_scenario(self):
{code_body}
"""

        if test_type == "API" and context == "API_DISK_DETACH":
             code_body = f"""        # Arrange
        base_url = "https://compute.api.cloud.ru"
        
        # Configuration
        disk_id = os.getenv("TEST_DISK_ID")
        vm_id = os.getenv("TEST_VM_ID")
        token = os.getenv("CLOUD_API_TOKEN")
        
        # Validation
        error_msg = "Please set TEST_DISK_ID and TEST_VM_ID in your .env file"
        assert disk_id, error_msg
        assert vm_id, error_msg
        
        endpoint = f"/api/v1/disks/{{disk_id}}/detach"
        
        headers = {{
            "Authorization": f"Bearer {{token}}",
            "Content-Type": "application/json"
        }}
        
        payload = {{
            "vm_id": vm_id
        }}

        # Act
        with allure.step(f"POST {{endpoint}}"):
            response = requests.post(base_url + endpoint, headers=headers, json=payload)

        # Assert
        with allure.step("Check Status Code 200"):
            assert response.status_code == 200, f"Expected 200, got {{response.status_code}}"
        
        data = response.json()
        
        with allure.step("Validate Response Schema"):
            assert "id" in data, "Response missing 'id'"
            assert data["id"] == disk_id, "ID mismatch"
            assert "vms" in data, "Response missing 'vms' list"
            assert isinstance(data["vms"], list), "'vms' must be a list"

        with allure.step("Validate Detachment"):
            # Check if the VM is NO LONGER in the 'vms' list
            attached_vm_ids = [vm["id"] for vm in data["vms"]]
            assert vm_id not in attached_vm_ids, f"VM {{vm_id}} should be detached but found in list"
        """
             
             decorators = f"""@allure.feature("{feature_name}")
@allure.story("Story: {feature_name}")
@allure.suite("API")
@allure.link("https://jira.cloud.ru/browse/TASK-API-DISK-DETACH", name="API Docs")"""

             return f"""{api_imports}

{decorators}
class Test{feature_name}:
    @allure.title("API Test: Detach Disk from VM")
    @allure.link("https://jira.cloud.ru/browse/TASK-PENDING", name="Related Task")
    @allure.tag("{priority.upper()}")
    @allure.label("priority", "{priority.lower()}")
    def test_scenario(self):
{code_body}
"""

        if test_type == "API" and context == "API_FLAVORS_LIST":
             code_body = f"""        # Arrange
        base_url = "https://compute.api.cloud.ru"
        endpoint = "/api/v1/flavors"
        
        # Configuration
        token = os.getenv("CLOUD_API_TOKEN")
        
        headers = {{
            "Authorization": f"Bearer {{token}}",
            "Content-Type": "application/json"
        }}
        
        params = {{
            "limit": 10,
            "order_by": "created_time",
            "order_desc": "true"
        }}

        # Act
        with allure.step(f"GET {{endpoint}}"):
            response = requests.get(base_url + endpoint, headers=headers, params=params)

        # Assert
        with allure.step("Check Status Code 200"):
            assert response.status_code == 200, f"Expected 200, got {{response.status_code}}"
        
        data = response.json()
        
        with allure.step("Validate Response Schema"):
            assert "items" in data, "Response missing 'items' field"
            assert isinstance(data["items"], list), "'items' must be a list"
            assert "total" in data, "Response missing 'total' field"
            assert "limit" in data
            assert "offset" in data
            
        with allure.step("Validate Flavor Item Structure"):
            if data["items"]:
                flavor = data["items"][0]
                assert "id" in flavor, "Flavor missing 'id'"
                assert "name" in flavor, "Flavor missing 'name'"
                assert "cpu" in flavor, "Flavor missing 'cpu'"
                assert "ram" in flavor, "Flavor missing 'ram'"
                assert "type" in flavor, "Flavor missing 'type'"
                assert "availability_zones" in flavor, "Flavor missing 'availability_zones'"
        """
             
             decorators = f"""@allure.feature("{feature_name}")
@allure.story("Story: {feature_name}")
@allure.suite("API")
@allure.link("https://jira.cloud.ru/browse/TASK-API-FLAVORS-LIST", name="API Docs")"""

             return f"""{api_imports}

{decorators}
class Test{feature_name}:
    @allure.title("API Test: Get Flavors List")
    @allure.link("https://jira.cloud.ru/browse/TASK-PENDING", name="Related Task")
    @allure.tag("{priority.upper()}")
    @allure.label("priority", "{priority.lower()}")
    def test_scenario(self):
{code_body}
"""









        if test_type == "API" and context == "API_FLAVORS_DETAILS":
             code_body = f"""        # Arrange
        base_url = "https://compute.api.cloud.ru"
        
        # Configuration
        flavor_id = os.getenv("TEST_FLAVOR_ID")
        token = os.getenv("CLOUD_API_TOKEN")
        
        # Validation
        error_msg = "Please set TEST_FLAVOR_ID in your .env file"
        assert flavor_id, error_msg
        
        endpoint = f"/api/v1/flavors/{{flavor_id}}"
        
        headers = {{
            "Authorization": f"Bearer {{token}}",
            "Content-Type": "application/json"
        }}

        # Act
        with allure.step(f"GET {{endpoint}}"):
            response = requests.get(base_url + endpoint, headers=headers)

        # Assert
        with allure.step("Check Status Code 200"):
            assert response.status_code == 200, f"Expected 200, got {{response.status_code}}"
        
        data = response.json()
        
        with allure.step("Validate Response Schema"):
            assert "id" in data, "Response missing 'id'"
            assert data["id"] == flavor_id, "ID mismatch"
            assert "name" in data, "Response missing 'name'"
            assert "cpu" in data, "Response missing 'cpu'"
            assert "ram" in data, "Response missing 'ram'"
            assert "type" in data, "Response missing 'type'"
            assert "availability_zones" in data, "Response missing 'availability_zones'"
            assert isinstance(data["availability_zones"], list), "'availability_zones' must be a list"
        """
             
             decorators = f"""@allure.feature("{feature_name}")
@allure.story("Story: {feature_name}")
@allure.suite("API")
@allure.link("https://jira.cloud.ru/browse/TASK-API-FLAVORS-DETAILS", name="API Docs")"""

             return f"""{api_imports}

{decorators}
class Test{feature_name}:
    @allure.title("API Test: Get Flavor Details")
    @allure.link("https://jira.cloud.ru/browse/TASK-PENDING", name="Related Task")
    @allure.tag("{priority.upper()}")
    @allure.label("priority", "{priority.lower()}")
    def test_scenario(self):
{code_body}
"""
        
        arrange_steps = [f'with allure.step("{start_step_title}"):']
        act_steps = []
        assert_steps = []
        
        for step in normalized_steps:
                lower_step = step.lower()
                
                def quote(text):
                    return f"'{text}'" if '"' in text else f'"{text}"'

                if "кнопка" in lower_step and ("кликабельна" in lower_step or "доступна" in lower_step):
                    clean_step = step.replace("доступна и кликабельна", "").replace("доступна", "").replace("кликабельна", "").strip(" .")
                    if "кнопка" in lower_step: clean_step = clean_step.replace("Кнопка", "кнопку")
                    
                    act_msg = f"Нажать на {clean_step}"
                    act_steps.append(f'with allure.step({quote(act_msg)}):')
                    
                    assert_txt = step.lower().replace("кликабельна", "доступна и кликабельна").strip(". ")
                    assert_msg = f"Убедиться, что {assert_txt}."
                    assert_steps.insert(0, f'with allure.step({quote(assert_msg)}):')
                    continue

                if any(x in lower_step for x in ['нажать', 'click', 'press', 'tap', 'ввести', 'enter', 'выбрать', 'перейти']):
                    act_steps.append(f'with allure.step({quote(step)}):')
                elif any(x in lower_step for x in ['открыть', 'open', 'start', 'login', 'войти']):
                    arrange_steps.append(f'with allure.step({quote(step)}):')
                else:
                    assert_steps.append(f'with allure.step({quote(step)}):')

        if not act_steps:
             if context == "CATALOG": act_steps.append('with allure.step("Выбрать продукт или применить фильтр"):')
             elif context == "CONFIG": act_steps.append('with allure.step("Изменить параметры конфигурации (CPU/RAM)"):')
             elif context == "MANAGEMENT": act_steps.append('with allure.step("Добавить или удалить сервис из конфигурации"):')
             elif context == "MOBILE": act_steps.append('with allure.step("Проверить доступность элементов управления"):')

        def build_block(steps):
            code = ""
            for s in steps: code += f"        {s}\n            pass\n"
            return code
            
        story_name = f"Story: {feature_name}" 

        return f"""import pytest
import allure

@allure.manual
@allure.label("owner", "{owner}")
@allure.feature("{feature_name}")
@allure.story("{story_name}")
@allure.suite("{test_type}")
@pytest.mark.manual
class Test{feature_name}:
    @allure.title("Test based on requirements")
    @allure.link("https://jira.cloud.ru/browse/TASK-PENDING", name="Related Task")
    @allure.tag("{priority.upper()}")
    @allure.label("priority", "{priority.lower()}")
    def test_scenario(self):
        # Arrange
{build_block(arrange_steps)}
        # Act
{build_block(act_steps)}
        # Assert
{build_block(assert_steps)}
"""

class OpenAIProvider(AIProvider):
    def __init__(self):
        pass
        
    async def generate_test_case(self, prompt: str) -> str:
        
        content = "```python\n# OpenAI Generated Code\n```"
        return self._clean_code(content)

def get_ai_provider() -> AIProvider:
    if settings.AI_PROVIDER == "openai":
        return OpenAIProvider()
    return MockAIProvider()
